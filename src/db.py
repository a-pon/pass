from typing import Annotated, Callable, Union

from fastapi import Depends
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from src.config import settings


class InternalError(Exception):
    pass


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except InternalError:
            await session.rollback()


def create_sessionmaker(
        bind_engine: Union[AsyncEngine, AsyncConnection]
) -> Callable[..., async_sessionmaker]:
    return async_sessionmaker(bind=bind_engine,
                              class_=AsyncSession,
                              expire_on_commit=False)


engine = create_async_engine(settings.db_url)
async_session = create_sessionmaker(engine)
db_dependency = Annotated[AsyncSession, Depends(get_async_session)]
