from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

database_client = AsyncIOMotorClient(
    f"mongodb://{settings.mongodb_username}:{settings.mongodb_password}@{settings.mongodb_host}:{settings.mongodb_port}"
)
mongo_database_con = database_client[settings.mongodb_database]
