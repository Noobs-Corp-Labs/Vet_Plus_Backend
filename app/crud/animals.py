from bson import ObjectId
from bson.errors import InvalidId

from app.schemas.animals import AnimalCreate
from app.database import mongo_database_con

async def insert_animal(animal_dto: AnimalCreate):
    try:
        create_result = await mongo_database_con["animals"].insert_one(animal_dto.model_dump(mode='json'))
        return str(create_result.inserted_id)
    except Exception as e:
        print(f"Erro ao criar animal: {e}")
        return None
    
async def find_all_animals():
    pipeline = [
        {
            "$lookup": {
                "from": "breeds",
                "let": {"breedId": {"$toObjectId": "$breed_id"}},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$_id", "$$breedId"]}}}
                ],
                "as": "breed"
            }
        },
        {
            "$unwind": {
                "path": "$breed",
                "preserveNullAndEmptyArrays": True  # mantém mesmo se não tiver breed
            }
        }
    ]
    animals = await mongo_database_con["animals"].aggregate(pipeline).to_list(length=None)
    return animals


async def find_one_animal(animal_identifier: str):
    try:
        filter_query = {
            "$or": [
                {"name": animal_identifier}
            ]
        }
        try:
            filter_query["$or"].append({"_id": ObjectId(animal_identifier)})
        except (InvalidId, Exception):
            pass

        pipeline = [
            {"$match": filter_query},
            {
                "$lookup": {
                    "from": "breeds",
                    "let": {"breedId": {"$toObjectId": "$breed_id"}},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$_id", "$$breedId"]}}}
                    ],
                    "as": "breed"
                }
            },
            {
                "$unwind": {
                    "path": "$breed",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {"$limit": 1}
        ]

        result = await mongo_database_con["animals"].aggregate(pipeline).to_list(length=1)
        return result[0] if result else None

    except Exception as e:
        print(f"Erro ao buscar animal: {e}")
        return None