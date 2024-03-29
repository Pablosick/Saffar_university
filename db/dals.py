from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from sqlalchemy.dialects.postgresql import UUID
from typing import Union
from sqlalchemy import update, and_, select

# Блок для взаимодействия с базой данных в бизнес контексте


class UserDataAccessLayer:
    """Создание пользователей, удаление пользователей и т.д. """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, name: str, surname: str, email: str) -> User:
        new_user = User(name=name,
                        surname=surname,
                        email=email,
                        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = update(User).where(and_(User.user_id == user_id and
                                        User.is_active == True)).values(is_active=False).returning(User.user_id)
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        get_user = res.fetchone()
        if get_user is not None:
            return get_user[0]
