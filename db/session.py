import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from typing import Generator

# Блок для взаимодействия с БД

# Создание асинхронного движка для взаимодействия с БД
engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

# Создание объекта асинхронной сессии
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
