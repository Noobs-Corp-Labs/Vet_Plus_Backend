from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

MONGO_URI = f"mongodb://{settings.mongodb_username}:{settings.mongodb_password}@{settings.mongodb_host}:{settings.mongodb_port}/?authSource={settings.mongodb_database}"
database_client = AsyncIOMotorClient(MONGO_URI)
mongo_database_con = database_client[settings.mongodb_database]