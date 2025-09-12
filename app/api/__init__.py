from fastapi import APIRouter
from app.api import users, admin, health

api_router = APIRouter()

api_router.include_router(admin.router, prefix='/admin', tags=['admin'])
api_router.include_router(health.router, prefix='/health', tags=['health'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
