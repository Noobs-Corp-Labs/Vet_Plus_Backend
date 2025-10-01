from fastapi import APIRouter
from Backend.app.models.animals import Animal
from Backend.app.schemas.animals import AnimalCreate

router = APIRouter()

@router.post("/animals", response_model=Animal)
async def create_animal(animal: AnimalCreate):
    # lógica de salvar no Mongo
    new_animal = {**animal.dict(), "id": "generated_mongo_id"}
    return new_animal
