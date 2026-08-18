"""JWT authentication dependency."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from app.core.security import verify_token
from app.core.database import get_db
from app.models.user import User
from app.services.auth import UserService
from sqlalchemy.orm import Session
import uuid

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP bearer credentials
        db: Database session
        
    Returns:
        Current user
        
    Raises:
        HTTPException: If token invalid or user not found
    """
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
        )

    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


async def require_role(*roles: str):
    """Dependency to require specific roles.
    
    Args:
        *roles: Required role names
        
    Returns:
        Dependency function
    """

    async def check_role(current_user: User = Depends(get_current_user)) -> User:
        """Check if user has required role.
        
        Args:
            current_user: Current authenticated user
            
        Returns:
            Current user if authorized
            
        Raises:
            HTTPException: If user doesn't have required role
        """
        user_roles = {role.name for role in current_user.roles}
        if not user_roles.intersection(set(roles)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This operation requires one of these roles: {', '.join(roles)}",
            )
        return current_user

    return check_role
