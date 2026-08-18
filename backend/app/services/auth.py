"""Authentication service for user management and token operations."""

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User, Role, Permission, RoleType
from app.core.security import (
    hash_password,
    verify_password,
    validate_password,
    create_access_token,
)
from app.schemas.auth import CreateUserRequest, UpdateUserRequest
from fastapi import HTTPException, status
from typing import Optional
import uuid


class UserService:
    """Service for user management operations."""

    @staticmethod
    def create_user(
        db: Session,
        user_request: CreateUserRequest,
    ) -> User:
        """Create a new user.
        
        Args:
            db: Database session
            user_request: User creation request
            
        Returns:
            Created user
            
        Raises:
            HTTPException: If user already exists or password invalid
        """
        # Check if user already exists
        existing_user = db.execute(
            select(User).where(
                (User.username == user_request.username)
                | (User.email == user_request.email)
            )
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username or email already exists",
            )

        # Validate password
        is_valid, error_msg = validate_password(user_request.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg,
            )

        # Create user
        user = User(
            username=user_request.username,
            email=user_request.email,
            full_name=user_request.full_name,
            password_hash=hash_password(user_request.password),
            is_active=user_request.is_active,
            is_superuser=user_request.is_superuser,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username.
        
        Args:
            db: Database session
            username: Username to search for
            
        Returns:
            User or None if not found
        """
        return db.execute(
            select(User).where(User.username == username)
        ).scalars().first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User or None if not found
        """
        return db.execute(
            select(User).where(User.id == user_id)
        ).scalars().first()

    @staticmethod
    def authenticate_user(
        db: Session,
        username: str,
        password: str,
    ) -> Optional[User]:
        """Authenticate user with username and password.
        
        Args:
            db: Database session
            username: Username
            password: Password
            
        Returns:
            User if authentication successful, None otherwise
        """
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        if not user.is_active:
            return None
        return user

    @staticmethod
    def update_user(
        db: Session,
        user: User,
        update_request: UpdateUserRequest,
    ) -> User:
        """Update user information.
        
        Args:
            db: Database session
            user: User to update
            update_request: Update request data
            
        Returns:
            Updated user
        """
        if update_request.full_name is not None:
            user.full_name = update_request.full_name
        if update_request.email is not None:
            user.email = update_request.email
        if update_request.is_active is not None:
            user.is_active = update_request.is_active
        if update_request.password is not None:
            is_valid, error_msg = validate_password(update_request.password)
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg,
                )
            user.password_hash = hash_password(update_request.password)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def assign_role(
        db: Session,
        user: User,
        role: Role,
    ) -> User:
        """Assign a role to a user.
        
        Args:
            db: Database session
            user: User to assign role to
            role: Role to assign
            
        Returns:
            Updated user
        """
        if role not in user.roles:
            user.roles.append(role)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def remove_role(
        db: Session,
        user: User,
        role: Role,
    ) -> User:
        """Remove a role from a user.
        
        Args:
            db: Database session
            user: User to remove role from
            role: Role to remove
            
        Returns:
            Updated user
        """
        if role in user.roles:
            user.roles.remove(role)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def login(
        db: Session,
        username: str,
        password: str,
    ) -> Optional[tuple[User, str]]:
        """Authenticate user and return token.
        
        Args:
            db: Database session
            username: Username
            password: Password
            
        Returns:
            Tuple of (user, token) or None if authentication failed
        """
        user = UserService.authenticate_user(db, username, password)
        if not user:
            return None

        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})
        return user, access_token
