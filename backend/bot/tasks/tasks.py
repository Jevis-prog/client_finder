import asyncio

from config import DB_COMMENTS_TIMEOUT, DB_FAILED_COMMENTS_TIMEOUT
from logger import logging
from telethon import TelegramClient

from bot.const import ProcessingStatus
from bot.tasks.base import scheduler
from bot.utils.tasks import process_messages


logger = logging.getLogger('tasks')

TASK_COMMENT_LOCK = asyncio.Lock()
TASK_FAILED_LOCK = asyncio.Lock()


async def task_comment_analysis(client: TelegramClient) -> None:
    """Периодическая задача для анализа комментариев."""
    if TASK_COMMENT_LOCK.locked():
        return
    async with TASK_COMMENT_LOCK:
        try:
            await process_messages(client)
            logger.debug('task comment analysis has been finished')
        except Exception as e:
            logger.error(f'Critical error in task_comment_analysis: {e}')


async def task_failed_comment_analysis(client: TelegramClient) -> None:
    """Периодическая задача для повторного анализа комментариев обработанных с ошибкой."""
    if TASK_FAILED_LOCK.locked():
        return
    async with TASK_FAILED_LOCK:
        try:
            await process_messages(
                status=ProcessingStatus.FAILED,
                error_status=ProcessingStatus.BROKEN,
                client=client,
            )
        except Exception as e:
            logger.error(f'Critical error in task_failed_comment_analysis: {e}')


def setup_scheduler(client) -> None:
    """Настраивает планировщик задач."""
    scheduler.add_job(
        task_comment_analysis,
        'interval',
        seconds=DB_COMMENTS_TIMEOUT,
        args=[client],
    )
    scheduler.add_job(
        task_failed_comment_analysis,
        'interval',
        seconds=DB_FAILED_COMMENTS_TIMEOUT,
        args=[client],
    )
