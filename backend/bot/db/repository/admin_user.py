import datetime

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from bot.db.models import AdminUserModel
from bot.db.repository.base import BaseRepository


class AdminUsersRepository(BaseRepository):
    """Репозиторий пользователей админки."""

    async def get(
        self,
        user_id: int | None = None,
        username: str | None = None,
    ) -> AdminUserModel | None:
        stmt = select(AdminUserModel)
        if user_id is not None:
            stmt = stmt.where(AdminUserModel.id == user_id)
        if username is not None:
            stmt = stmt.where(AdminUserModel.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_create(self, username: str, password_hash: str) -> AdminUserModel:
        stmt = (
            insert(AdminUserModel)
            .values(username=username, password_hash=password_hash)
            .on_conflict_do_update(
                index_elements=['username'],
                set_={
                    'updated_at': datetime.datetime.now(),
                    'password_hash': password_hash,
                },
            )
            .returning(AdminUserModel)
        )
        orm_stmt = select(AdminUserModel).from_statement(stmt).execution_options(
            populate_existing=True,
        )
        result = await self.session.execute(orm_stmt)
        return result.scalar_one()

    async def update(self, user_id: int, **values: AdminUserModel) -> None:
        stmt = update(AdminUserModel).values(**values).where(AdminUserModel.id == user_id)
        await self.session.execute(stmt)
