from typing import Any


class BaseUnitOfWork:
    """Базовый класс единицы работы."""

    async def __aenter__(self) -> 'BaseUnitOfWork':
        """Инициализация контекстного менеджера."""
        return self  # pragma: no cover

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Выход из контекстного менеджера."""
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.shutdown()

    async def commit(self) -> None:
        """Применение изменений."""

    async def rollback(self) -> None:
        """Откат изменений."""

    async def shutdown(self) -> None:
        """Закрытие ресурса."""
