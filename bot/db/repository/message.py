from typing import Sequence

from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from bot.const import ProcessingStatus
from bot.db import MessageModel
from bot.db.repository.base import BaseRepository


class MessagesHandler(BaseRepository):
    """Репозиторий сообщений."""

    async def save_message_to_db(
        self,
        sender_id: int,
        chat_id: int,
        external_id: int,
        message_text: str,
        processing_status: ProcessingStatus,
    ) -> None:
        """Сохранение сообщения в бд."""
        stmt = (
            insert(MessageModel)
            .values(
                sender_id=sender_id,
                chat_id=chat_id,
                external_id=external_id,
                message_text=message_text,
                processing_status=processing_status,
            )
            .returning(MessageModel.id)
        )
        await self.session.execute(stmt)

    async def get_unprocessed_messages(
        self,
        status: ProcessingStatus = ProcessingStatus.PENDING,
    ) -> Sequence[MessageModel]:
        """Получает еще не проанализированные/зафейленые нейросетью сообщения из бд."""
        query = (
            select(MessageModel)
            .options(selectinload(MessageModel.chat), selectinload(MessageModel.user))
            .where(MessageModel.processing_status == status)
            .order_by(MessageModel.created_at)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def bulk_updating_messages(
        self,
        ids: list[int],
        status: ProcessingStatus,
        is_lead: bool | None = None,
        reason: str | None = None,
    ) -> None:
        """Обновляет статусы сообщений и дополнительную информацию о лидах."""
        update_values = {'processing_status': status}
        if is_lead is not None:
            update_values['is_lead'] = is_lead
        if reason is not None:
            update_values['reason'] = reason

        stmt = (
            update(MessageModel)
            .where(MessageModel.id.in_(ids))
            .values(**update_values)
        )
        await self.session.execute(stmt)
