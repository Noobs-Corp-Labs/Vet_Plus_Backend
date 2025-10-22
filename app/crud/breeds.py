from bson import ObjectId
from bson.errors import InvalidId

from app.database import mongo_database_con

async def find_all_breeds():
    breeds = await mongo_database_con["breeds"].find().to_list(length=None)
    return breeds
    
async def find_one_breed(breed_identifier: str):
    filter_query = {"$or": [{"name": breed_identifier}]}
    try:
        filter_query["$or"].append({"_id": ObjectId(breed_identifier)})
    except (InvalidId, Exception):
        pass
    
    breed = await mongo_database_con["breeds"].find_one(filter=filter_query)
    return breed