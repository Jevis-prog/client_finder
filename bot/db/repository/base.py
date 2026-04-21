from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """Базовый класс репозитория."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
