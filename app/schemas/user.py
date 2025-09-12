from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

from app.models.user import User

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8)

    @validator('password')
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

    @validator('password')
    def validate_password(cls, v):
        if v is None:
            return v
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must include a digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must include an uppercase letter')
        return ValueError('Password must include an uppercase letter')

class UserResponse(User):
    class Config(User.Config):
        # quando usar .dict() ou FastAPI para serializar, exclui automaticamente
        fields = {
            'hashed_password': {'exclude': True}
        }
