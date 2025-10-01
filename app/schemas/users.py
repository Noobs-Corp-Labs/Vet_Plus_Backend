from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

from Backend.app.models.users import User

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8)

    @field_validator('password')
    def validate_password(cls, v):
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must include a digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must include an uppercase letter')
        return v

class UserUpdate(BaseModel):
    id: str
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[str] = Field(None, min_length=8)

    @field_validator('password')
    def validate_password(cls, v):
        if v is None:
            return v
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must include a digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must include an uppercase letter')
        return ValueError('Password must include an uppercase letter')

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    is_active: bool
    is_admin: bool
    created_at: str | None = None
    updated_at: str | None = None
