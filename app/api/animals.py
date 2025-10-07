from fastapi import APIRouter
from app.schemas.animals import AnimalCreate, AnimalResponse

router = APIRouter()

@router.post("/animals", response_model=AnimalResponse)
async def create_animal(animal: AnimalCreate):
    # lógica de salvar no Mongo
    new_animal = {**animal.dict(), "id": "generated_mongo_id"}
    return new_animal
