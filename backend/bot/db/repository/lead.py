from sqlalchemy import select
from sqlalchemy.orm import selectinload

from bot.const import ProcessingStatus
from bot.db.models import MessageModel
from bot.db.repository.base import BaseRepository


class LeadsRepository(BaseRepository):
    """Репозиторий лидов для админки."""

    async def list_leads(self, limit: int = 100) -> list[MessageModel]:
        stmt = (
            select(MessageModel)
            .options(
                selectinload(MessageModel.user),
                selectinload(MessageModel.chat),
            )
            .where(MessageModel.processing_status == ProcessingStatus.ANALYZED)
            .order_by(MessageModel.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
