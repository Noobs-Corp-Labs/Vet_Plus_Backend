from fastapi import APIRouter, HTTPException

from app.schemas.communs import ListResponse
from app.schemas.breeds import BreedResponse
from app.crud.breeds import find_all_breeds


router = APIRouter()

@router.get("/", response_model=ListResponse[BreedResponse])
async def get_all_breeds():
    try:
        breeds = await find_all_breeds()
        for breed in breeds:
            breed["_id"] = str(breed["_id"])

        return ListResponse(
            count=len(breeds),
            rows=breeds
        )
    
    except Exception as e:
        print(f"Erro ao buscar raças: {e}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao buscar raças."
        )
