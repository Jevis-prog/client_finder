from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncIterator

from config import DB_STR
from sqlalchemy import DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


async_engine = create_async_engine(DB_STR, future=True)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


@asynccontextmanager
async def session_context_manager() -> AsyncIterator[AsyncSession]:
    """Безопасно открывает сессию."""
    async with async_session() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    """Base model."""

    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
