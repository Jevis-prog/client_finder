import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from bot.db.models import ChatsModel
from bot.db.repository.base import BaseRepository


class ChatsRepository(BaseRepository):
    """Репозиторий чатов бота."""

    async def get_or_create(self, external_id: int, chat_title: str) -> ChatsModel:
        """Создать или получить группу."""
        stmt = (
            insert(ChatsModel)
            .values(external_id=external_id, chat_title=chat_title)
            .on_conflict_do_update(
                index_elements=['external_id'],
                set_={
                    'updated_at': datetime.datetime.now(),
                    'chat_title': chat_title,
                },
            )
            .returning(ChatsModel)
        )
        orm_stmt = select(ChatsModel).from_statement(stmt).execution_options(populate_existing=True)
        result = await self.session.execute(orm_stmt)
        return result.scalar_one()
