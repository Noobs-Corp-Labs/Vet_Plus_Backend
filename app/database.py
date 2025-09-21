from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

database_client = AsyncIOMotorClient(
    f"mongodb://{settings.mongodb_username}:{settings.mongodb_password}@{settings.mongodb_host}:{settings.mongodb_port}/{settings.mongodb_database}?authSource={settings.mongodb_database}"
)
mongo_database_con = database_client
