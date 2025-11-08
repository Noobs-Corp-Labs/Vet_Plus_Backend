from fastapi import APIRouter, HTTPException, status
from app.schemas.users import UserCreate, UserResponse, UserUpdate
from app.crud.users import create_user, get_user_by_email, get_users, get_user, update_user, delete_user

router = APIRouter()

# DEV: Criar funcs no /services para post user, update user, delete user.

@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    # DEV: Adicionar outros tipos de validação ao criar usuário.
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return await create_user(user)

@router.get('/', response_model=list[UserResponse])
async def read_users(skip: int = 0, limit: int = 100):
    return await get_users(skip=skip, limit=limit)


@router.get('/{user_id}', response_model=UserResponse)
async def read_user(user_id: str):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@router.put('/{user_id}', response_model=UserResponse)
async def modify_user(user_id: str, user: UserUpdate):
    #DEV: Adicionar a func as validação de update de user infos
    updated_user = await update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail='User not found')
    return updated_user

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(user_id: str):
    #DEV: Adicionar a func as validação para delete de user antes de chamar o delete
    deleted = await delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='User not found')
    return None
