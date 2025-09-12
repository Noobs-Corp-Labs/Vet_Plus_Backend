from fastapi import APIRouter
from app.services.health import check_system

router = APIRouter()

@router.get('/liveness')
async def liveness():
    return {'status': 'alive'}

@router.get('/readiness')
async def readiness():
    return await check_system()