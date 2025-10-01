from pydantic import BaseModel

class User(BaseModel):
    id: str | None = None
    email: str
    name: str
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        from_attributes = True
