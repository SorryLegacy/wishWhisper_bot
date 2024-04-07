from datetime import datetime
from typing import AsyncGenerator, Annotated, Any


from fastapi import Depends
from sqlalchemy import BigInteger, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import config


Base = declarative_base()

engine = create_async_engine(config.DATABASE_URI.unicode_string())

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session


db_depend = Annotated[Any, Depends(get_session)]


class AbstarctModel(Base):
    """
    Abstarct model with `id` and `created`
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, autoincrement=False, primary_key=True)
    created: Mapped[datetime] = mapped_column(server_default=func.now())
