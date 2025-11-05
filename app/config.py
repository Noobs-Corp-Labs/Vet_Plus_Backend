from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # FastAPI
    swagger_servers_list: Optional[str] = None

    # Server
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # MongoDB
    mongodb_host: str
    mongodb_port: int
    mongodb_username: str
    mongodb_password: str
    mongodb_database: str

    # Gemini
    gemini_api_key: str
    gemini_model: str

    class Config:
        env_file = ".env"

settings = Settings()
