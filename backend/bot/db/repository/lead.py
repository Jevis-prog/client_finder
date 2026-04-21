from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from bot.const import ProcessingStatus
from bot.db.models import MessageModel
from bot.db.repository.base import BaseRepository


class LeadsRepository(BaseRepository):
    """Репозиторий лидов для админки."""

    async def list_leads(self, only_valid: bool = False, limit: int = 100) -> list[MessageModel]:
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
        if only_valid:
            stmt = stmt.where(MessageModel.is_lead.is_(True))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_stats(self) -> dict[str, int]:
        now = datetime.utcnow()
        day_ago = now - timedelta(days=1)
        hour_ago = now - timedelta(hours=1)

        total_messages = await self.session.scalar(select(func.count(MessageModel.id)))
        processed_messages = await self.session.scalar(
            select(func.count(MessageModel.id)).where(
                MessageModel.processing_status != ProcessingStatus.PENDING,
            ),
        )
        total_leads = await self.session.scalar(
            select(func.count(MessageModel.id)).where(
                MessageModel.processing_status == ProcessingStatus.ANALYZED,
            ),
        )
        valid_leads = await self.session.scalar(
            select(func.count(MessageModel.id)).where(
                MessageModel.processing_status == ProcessingStatus.ANALYZED,
                MessageModel.is_lead.is_(True),
            ),
        )
        processed_last_day = await self.session.scalar(
            select(func.count(MessageModel.id)).where(
                MessageModel.processing_status != ProcessingStatus.PENDING,
                MessageModel.updated_at >= day_ago,
            ),
        )
        processed_last_hour = await self.session.scalar(
            select(func.count(MessageModel.id)).where(
                MessageModel.processing_status != ProcessingStatus.PENDING,
                MessageModel.updated_at >= hour_ago,
            ),
        )

        return {
            'total_messages': total_messages or 0,
            'processed_messages': processed_messages or 0,
            'total_leads': total_leads or 0,
            'valid_leads': valid_leads or 0,
            'processed_last_day': processed_last_day or 0,
            'processed_last_hour': processed_last_hour or 0,
        }
