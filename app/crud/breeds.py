from app.database import mongo_database_con

async def find_all_breeds():
    breed = await mongo_database_con["breeds"].find().to_list(length=None)
    return breed
    