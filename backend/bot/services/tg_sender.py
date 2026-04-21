from config import TARGET_CHAT_ID
from logger import logging
from telethon import TelegramClient
from telethon.errors import RPCError

from bot.utils.schemas import MessageAnalysis


logger = logging.getLogger('tg_service')


async def send_lead_message(
    lead_messages: list[MessageAnalysis],
    client: TelegramClient,
    target_chat_id: int = TARGET_CHAT_ID,
) -> None:
    """Отправка лидов в чат."""
    if not client.is_connected():
        await client.start()

    for msg in lead_messages:
        try:

            text = (
                f'ID: {msg.id}\n\n'
                f'Источник: {msg.chat_title}\n\n'
                f'Отправитель: {msg.sender_username or "Неизвестный пользователь"}\n\n'
                f'Сообщение: {msg.message_text}\n\n'
                f'Причина: {msg.result.reason}'
            )

            await client.send_message(target_chat_id, text)

        except RPCError as e:
            logger.error(f'[Telethon] RPCError ошибка с msg_id={msg.message_id}: {e!r}')
        except Exception as e:
            logger.exception(f'[Telethon] Ошибка с msg_id={msg.message_id}: {e!r}')
