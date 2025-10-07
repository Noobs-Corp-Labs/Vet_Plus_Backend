from datetime import datetime
from bson import ObjectId
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate
from app.services.auth import get_password_hash
from app.database import mongo_database_con

# --------------------------
# Funções CRUD para MongoDB
# --------------------------

async def get_user(user_id: str) -> User:
    """Retorna um usuário pelo _id"""
    user = await mongo_database_con["users"].find_one({"_id": ObjectId(user_id)})
    if user:
        return User(**user)
    return None

async def get_user_by_email(email: str) -> User:
    """Retorna um usuário pelo email"""
    user = await mongo_database_con["users"].find_one({"email": email})
    if user:
        return User(**user)
    return None

async def get_users(skip: int = 0, limit: int = 100) -> list[User]:
    """Retorna todos os usuários com paginação"""
    users = await mongo_database_con["users"].find().skip(skip).limit(limit).to_list(length=limit)
    return [User(**u) for u in users]

async def create_user(user: UserCreate):
    """Cria um usuário"""
    hashed_password = get_password_hash(user.password)
    user_doc = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
    )
    result = await mongo_database_con["users"].insert_one(user_doc.dict())
    user_doc.id = str(result.inserted_id)
    return user_doc

async def update_user(user: UserUpdate) -> User | None:
    """Atualiza um usuário pelo _id"""
    data = user.dict(exclude_unset=True, exclude={"id"})
    if "password" in data:
        data["hashed_password"] = get_password_hash(data.pop("password"))
    data["updated_at"] = datetime.utcnow().isoformat()
    result = await mongo_database_con["users"].update_one(
        {"_id": ObjectId(user.id)},
        {"$set": data}
    )
    if result.matched_count == 0:
        return None
    updated_user = await mongo_database_con["users"].find_one({"_id": ObjectId(user.id)})
    return User(**updated_user)

async def delete_user(user_id: str) -> bool:
    """Deleta um usuário pelo _id"""
    result = await mongo_database_con["users"].delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0
