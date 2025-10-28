from bson import ObjectId
from bson.errors import InvalidId

from app.database import mongo_database_con

async def validate_animal_exists(animal_id: str) -> bool:
    """
    Valida se existe um animal com o ID informado
    Args: animal_id: ID do animal (string)
    Returns: True se o animal existe, False caso contrário
    """
    try:
        object_id = ObjectId(animal_id)

        animal = await mongo_database_con["animals"].find_one(
            {"_id": object_id},
            {"_id": 1}
        )
        
        return animal is not None
        
    except (InvalidId, Exception):
        return False