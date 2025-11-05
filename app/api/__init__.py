from fastapi import APIRouter
from app.api import animals, breeds, events, gemini, users, admin, health

api_router = APIRouter()

api_router.include_router(admin.router, prefix='/admin', tags=['Admin'])
api_router.include_router(gemini.router, prefix='/gemini', tags=['Gemini'])
api_router.include_router(events.router, prefix='/events', tags=['Events'])
api_router.include_router(animals.router, prefix='/animals', tags=['Animals'])
api_router.include_router(breeds.router, prefix='/breeds', tags=['Breeds'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(health.router, prefix='/health', tags=['Health'])
