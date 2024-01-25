import settings
import pytest
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Создание асинхронного движка для взаимодействия с тестовой БД
test_engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)

# Создание объекта асинхронной сессии с тестовой БД
async_test_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

CLEAN_TABLES = [
    "users"
]


@pytest.fixture(scope="session", autouse=True)
async def run_migration():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migration"')
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True))
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_table(async_session_test):
    """Очистка данных во всех таблицах перед запуском тестовой функции"""
    async with async_session_test as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(f"""TRUNCATE TABLE {table_for_cleaning}""")

