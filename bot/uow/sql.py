from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.db import async_session
from bot.db.repository.group import ChatsRepository
from bot.db.repository.message import MessagesHandler
from bot.db.repository.user import UsersRepository
from bot.uow.base import BaseUnitOfWork


class SQLUoW(BaseUnitOfWork):
    """Единица работы с базой данных."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] = async_session,
    ) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> 'SQLUoW':
        """Открытие контекстного менеджера."""
        self.session: AsyncSession = self.session_factory()
        self.message_repo = MessagesHandler(self.session)
        self.user_repo = UsersRepository(self.session)
        self.chat_repo = ChatsRepository(self.session)
        await super().__aenter__()
        return self

    async def commit(self) -> None:
        """Применение изменений."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Откат изменений."""
        await self.session.rollback()

    async def close(self) -> None:
        """Закрытие сессии."""
        await self.session.close()
