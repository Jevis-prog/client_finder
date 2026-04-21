import asyncio
from typing import Generator

from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL
from logger import logging
from telethon import TelegramClient

from bot.const import ProcessingStatus
from bot.exceptions import AiClientError
from bot.services.ai_client import AIService, OpenAIClientAdapter
from bot.services.tg_sender import send_lead_message
from bot.uow.sql import SQLUoW
from bot.utils.schemas import MessageAnalysis, MessageForAnalyzeStatus


logger = logging.getLogger('tasks')

TASK_RUNNING = asyncio.Lock()
BATCH_SIZE = 2000


def batch_generator(
        messages: list[MessageAnalysis],
        batch_size: int,
) -> Generator[list[MessageAnalysis], None, None]:
    """Отдает чанки по длине токенов."""
    bucket = []
    bucket_size = 0

    for msg in messages:
        if msg.length + bucket_size < batch_size:
            bucket.append(msg)
            bucket_size += msg.length
        else:
            if bucket:
                yield bucket
            bucket = [msg]
            bucket_size = msg.length
    if bucket:
        yield bucket


async def analyze_messages_batch(
    messages: list[MessageAnalysis],
) -> None:
    """Анализ сообщений через AI сервис с обработкой чанков и объединением результатов."""
    ai_client = AIService(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_API_URL,
        model=DEEPSEEK_MODEL,
        client=OpenAIClientAdapter,
    )

    # Разбиваем сообщения на чанки
    for chunk in batch_generator(messages, batch_size=BATCH_SIZE):
        try:
            # Получаем обновленные объекты с анализом
            response_map = await ai_client.analyze_messages(chunk)
            # Обновляем статус сообщений на SUCCESS
            for msg in chunk:
                if msg.id in response_map:
                    analyzed = response_map[msg.id]
                    msg.result = analyzed.result
                    msg.status = MessageForAnalyzeStatus.SUCCESS

        except AiClientError as e:
            logger.error(f'Error analyzing chunk of messages: {repr(e)}')


async def process_messages(
        client: TelegramClient,
        status: ProcessingStatus = ProcessingStatus.PENDING,
        error_status: ProcessingStatus = ProcessingStatus.FAILED,
) -> list[MessageAnalysis] | None:
    """Обработка сообщений."""
    async with SQLUoW() as uow:
        pending_messages = await uow.message_repo.get_unprocessed_messages(status=status)

    if not pending_messages:
        return

    messages_batch = [
        MessageAnalysis(
            sender_id=str(msg.sender_id),
            sender_username=msg.user.username,
            message_text=msg.message_text,
            id=msg.id,
            chat_id=msg.chat_id,
            chat_title=msg.chat.chat_title,
            message_id=msg.external_id,
        )
        for msg in pending_messages
    ]

    await analyze_messages_batch(messages_batch)

    # Формируем списки для обновлений: лиды (объекты), не‑лиды и ошибки
    lead_messages: list[MessageAnalysis] = []
    non_leads: list[MessageAnalysis] = []
    failed_ids: list[int] = []

    for msg in messages_batch:
        if msg.status == MessageForAnalyzeStatus.SUCCESS:
            if msg.result.is_lead:
                lead_messages.append(msg)
            else:
                non_leads.append(msg)
        else:
            failed_ids.append(msg.id)

    await send_lead_message(lead_messages=lead_messages, client=client)

    # Обновление статусов в БД
    async with SQLUoW() as uow:
        # Обновляем успешные лиды по одному (у каждого свой reason)
        if lead_messages:
            for m in lead_messages:
                await uow.message_repo.bulk_updating_messages(
                    ids=[m.id],
                    status=ProcessingStatus.ANALYZED,
                    is_lead=True,
                    reason=m.result.reason,
                )
            logger.info(f'Marked {len(lead_messages)} messages as ANALYZED (leads)')

        # Обновляем успешные не-лиды
        if non_leads:
            for m in non_leads:
                await uow.message_repo.bulk_updating_messages(
                    ids=[m.id],
                    status=ProcessingStatus.ANALYZED,
                    is_lead=False,
                    reason=m.result.reason,
                )
            logger.info(f'Marked {len(non_leads)} messages as ANALYZED (non-leads)')

        # Обновляем неудачные сообщения
        if failed_ids:
            await uow.message_repo.bulk_updating_messages(
                ids=failed_ids,
                status=error_status,
                is_lead=False,
            )
            logger.info(f'Marked {len(failed_ids)} messages as {error_status}')

    return messages_batch
