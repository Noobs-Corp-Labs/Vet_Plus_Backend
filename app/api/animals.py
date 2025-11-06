from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status

from app.schemas.communs import ListResponse
from app.crud.breeds import find_one_breed
from app.crud.animals import find_all_animals, find_one_animal, insert_animal
from app.schemas.animals import AnimalCreate, AnimalResponse

router = APIRouter()

@router.post("/", 
    response_model=AnimalResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_animal(body: AnimalCreate):
    animal_id = await insert_animal(body)
    if not animal_id:
        raise HTTPException(
            status_code=500, 
            detail="Não foi possível criar o animal no banco de dados."
        )

    breed = await find_one_breed(body.breed_id)
    if not breed:
        raise HTTPException(
            status_code=404,
            detail=f"Raça com ID {body.breed_id} não encontrada."
        )
    
    if "_id" in breed:
        breed["_id"] = str(breed["_id"])

    new_animal = {
        "_id": str(animal_id),
        **body.model_dump(),
        "breed": breed
    }
    return new_animal

@router.get("/", response_model=ListResponse[AnimalResponse])
async def get_all_animals():
    try:
        animals = await find_all_animals()
        for animal in animals:
            animal["_id"] = str(animal["_id"])
            if animal.get("breed") and "_id" in animal["breed"]:
                animal["breed"]["_id"] = str(animal["breed"]["_id"])

        return ListResponse(
            count=len(animals),
            rows=animals
        )
    
    except Exception as e:
        print(f"Erro ao buscar animais: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao buscar animais."
        )

@router.get("/{animal_identifier}",
    response_model=AnimalResponse,
    status_code=status.HTTP_200_OK,
)
async def get_one_animal(
    animal_identifier: Annotated[
        str,
        Path(
            description="Name or Id of the animal to retrieve",
            example="String"
        )
    ]
):
    try:
        animal_obj = await find_one_animal(animal_identifier)
        if not animal_obj:
            raise HTTPException(status_code=404, detail='Animal not found')
        animal_obj["_id"] = str(animal_obj["_id"])
        animal_obj["breed"]["_id"] = str(animal_obj["breed"]["_id"])
        return animal_obj
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao buscar dados do animal: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao buscar dados do animal."
        )
