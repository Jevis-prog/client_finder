import datetime

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from bot.db.models import UserModel
from bot.db.repository.base import BaseRepository


class UsersRepository(BaseRepository):
    """Репозиторий пользователей бота."""

    async def get_or_create(self, external_id: int, username: str) -> UserModel:
        """Создать или получить текущего пользователя."""
        stmt = (
            insert(UserModel)
            .values(external_id=external_id, username=username)
            .on_conflict_do_update(
                index_elements=['external_id'],
                set_={
                    'updated_at': datetime.datetime.now(),
                    'username': username,
                },
            )
            .returning(UserModel)
        )
        orm_stmt = select(UserModel).from_statement(stmt).execution_options(populate_existing=True)
        result = await self.session.execute(orm_stmt)
        return result.scalar_one()

    async def update(self, user_id: int, **values: UserModel) -> None:
        """Обновить информацию о пользователе."""
        stmt = update(UserModel).values(**values).where(UserModel.id == user_id)
        await self.session.execute(stmt)
