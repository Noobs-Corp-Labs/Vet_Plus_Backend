from fastapi import APIRouter, HTTPException, Path, status
from typing import Annotated

from app.schemas.communs import ListResponse
from app.schemas.breeds import BreedResponse
from app.crud.breeds import find_all_breeds, find_one_breed


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

@router.get("/{breed_identifier}",
    response_model=BreedResponse,
    status_code=status.HTTP_200_OK,
)
async def get_one_breed(
    breed_identifier: Annotated[
        str,
        Path(
            description="Name or Id of the breed to retrieve",
            example="String"
        )
    ]
):
    breed_obj = await find_one_breed(breed_identifier)
    if not breed_obj:
        raise HTTPException(status_code=404, detail='Breed not found')
    breed_obj["_id"] = str(breed_obj["_id"])
    return breed_obj