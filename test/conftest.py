import asyncio
import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_async_session

# URL к вашей базе в Docker
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db_test:5432/weather_test"

@pytest_asyncio.fixture(scope="session")
async def engine():
    """Создаем движок внутри фикстуры, чтобы он привязался к текущему циклу событий."""
    engine = create_async_engine(TEST_DATABASE_URL)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="session")
async def session_maker(engine):
    """Создаем фабрику сессий."""
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_database(engine):
    """Автоматическое создание и удаление таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="session")
async def ac(session_maker):
    """Клиент для тестов с подменой зависимости БД."""
    
    async def override_get_async_session():
        async with session_maker() as session:
            yield session

 
    app.dependency_overrides[get_async_session] = override_get_async_session
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as client:
        yield client
    

    app.dependency_overrides.clear()