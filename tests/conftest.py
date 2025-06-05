import asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.config import settings
from src.db import async_session
from src.models import Base

test_engine = create_async_engine(settings.db_url, echo=False)


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncSession:
    async with async_session() as session:
        yield session
