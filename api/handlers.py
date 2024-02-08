from fastapi import APIRouter, Depends, HTTPException
from .models import UserCreate, ShowUser, DeleteUserResponse, GetUser
from db.session import get_db
from db.dals import UserDataAccessLayer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from uuid import UUID

# Блок с роутами(путями) API
user_router = APIRouter()


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session:  # Создание сессии
        async with session.begin():
            user_dal = UserDataAccessLayer(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active
            )


async def _delete_user(user_id, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDataAccessLayer(session)
            deleted_user_id = await user_dal.delete_user(user_id=user_id)
            return deleted_user_id


async def _get_user(user_id, db) -> Union[ShowUser, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDataAccessLayer(session)
            get_user_by_id = await user_dal.get_user(user_id)
            if get_user_by_id is not None:
                return ShowUser(
                    user_id=get_user_by_id.id,
                    name=get_user_by_id.name,
                    surname=get_user_by_id.surname,
                    email=get_user_by_id.email,
                    is_active=get_user_by_id.is_active
                )


@user_router.get("/", response_model=ShowUser)
async def get_user(body: GetUser, db: AsyncSession = Depends(get_db)):
    user = await _get_user(body, db)
    if user is None:
        raise HTTPException(status_code=404, detail="Ошибка получения данных о пользователе")
    return user


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    return await _create_new_user(body, db)


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> DeleteUserResponse:
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"Пользователь с {deleted_user_id} не найден")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)
