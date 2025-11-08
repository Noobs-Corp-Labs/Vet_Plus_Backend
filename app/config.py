from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # FastAPI
    swagger_servers_list: Optional[str] = None

    # Server
    secret_key: str = "devsecret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # MongoDB
    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    mongodb_username: str = "root"
    mongodb_password: str = "root"
    mongodb_database: str = "vetplus"

    # Gemini
    gemini_api_key: str = "fake"
    gemini_model: str = "gemini-test"

    class Config:
        env_file = ".env"

settings = Settings()