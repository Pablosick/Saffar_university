from fastapi import APIRouter, Depends
from .models import UserCreate, ShowUser
from db.session import get_db
from db.dals import UserDataAccessLayer
from sqlalchemy.ext.asyncio import AsyncSession


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


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    return await _create_new_user(body, db)
