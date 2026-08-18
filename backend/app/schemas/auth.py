"""Pydantic schemas for authentication endpoints."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid
from datetime import datetime


class LoginRequest(BaseModel):
    """Login request schema."""

    username: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """User response schema (for API responses)."""

    id: uuid.UUID
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateUserRequest(BaseModel):
    """Create user request schema."""

    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=255)
    password: str = Field(..., min_length=12)
    is_active: bool = True
    is_superuser: bool = False


class UpdateUserRequest(BaseModel):
    """Update user request schema."""

    full_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=12)


class RoleResponse(BaseModel):
    """Role response schema."""

    id: uuid.UUID
    name: str
    description: Optional[str] = None
    role_type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PermissionResponse(BaseModel):
    """Permission response schema."""

    id: uuid.UUID
    name: str
    description: Optional[str] = None
    resource: str
    action: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenPayload(BaseModel):
    """JWT token payload schema."""

    sub: str  # Subject (user ID)
    exp: int  # Expiration time
