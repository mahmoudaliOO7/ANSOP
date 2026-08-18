"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.config import get_settings
from app.models.user import User
from app.services.auth import AuthService, UserService
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    UserResponse,
    CreateUserRequest,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
settings = get_settings()


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate user and return JWT token.
    
    Args:
        request: Login credentials
        db: Database session
        
    Returns:
        Access token
        
    Raises:
        HTTPException: If authentication failed
    """
    result = AuthService.login(db, request.username, request.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    user, token = result
    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()

    return TokenResponse(
        access_token=token,
        expires_in=settings.jwt_expiration_minutes * 60,
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Get current authenticated user information.
    
    Args:
        current_user: Current user from JWT token
        
    Returns:
        Current user information
    """
    return UserResponse.from_orm(current_user)


@router.post("/users", response_model=UserResponse)
async def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Create a new user (admin only).
    
    Args:
        request: User creation request
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created user
        
    Raises:
        HTTPException: If user not admin or user already exists
    """
    # Check admin permission
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create users",
        )

    user = UserService.create_user(db, request)
    return UserResponse.from_orm(user)
