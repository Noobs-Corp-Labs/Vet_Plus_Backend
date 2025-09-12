from fastapi import APIRouter
from app.crud.stats import get_system_stats

from app.schemas.stats import StatsResponse

router = APIRouter()

@router.get('/dashboard', response_model=StatsResponse)
async def dashboard():
    return await get_system_stats()
