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
        collection = "users"
        indexes = [
            {"keys": [("email", 1)], "unique": True},
            {"keys": [("is_active", 1)]},
            {"keys": [("created_at", -1)]},
            {"keys": [("is_admin", 1), ("is_active", 1)]},
        ]
