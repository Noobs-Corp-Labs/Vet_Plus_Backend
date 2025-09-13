from fastapi import APIRouter
from app.api import users, admin, health

api_router = APIRouter()

api_router.include_router(admin.router, prefix='/admin', tags=['Admin'])
api_router.include_router(health.router, prefix='/health', tags=['Health'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
