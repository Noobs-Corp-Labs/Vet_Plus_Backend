from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Server
    root_path: Optional[str] = None
    swagger_servers_list: Optional[str] = None
    secret_key: str = '47dcffaa-7288-4669-ad67-f8399bc06b23'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30

    # MongoDB
    mongodb_host: str
    mongodb_port: int
    mongodb_username: str
    mongodb_password: str
    mongodb_database: str

    class Config:
        env_file = ".env"

settings = Settings()
