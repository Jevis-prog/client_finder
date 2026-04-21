import logging
from dataclasses import dataclass

from telethon import TelegramClient
from telethon.events import NewMessage

from bot.const import ProcessingStatus


logger = logging.getLogger('tg_service')


@dataclass(frozen=True)
class MessageInfo:
    """Информация о сообщении."""

    sender_id: int
    chat_id: int
    chat_title: str
    external_id: int
    message_text: str
    processing_status: ProcessingStatus


async def get_chat_data(event: NewMessage.Event) -> MessageInfo:
    """Получить данные по сообщению."""
    msg = event.message
    chat = await event.get_chat()
    return MessageInfo(
        sender_id=msg.sender_id,
        external_id=msg.id,
        message_text=msg.text,
        processing_status=ProcessingStatus.PENDING,
        chat_id=chat.id,
        chat_title=chat.title,
    )


async def get_chat_ids_and_names(client: TelegramClient) -> list[tuple[int, str]]:
    """Получение id и названий чатов."""
    await client.start()
    chats = []
    async for dialog in client.iter_dialogs():
        chats.append((dialog.id, dialog.name))
    return chats

async def show_chats(client: TelegramClient) -> None:
    """Выводит id и названия чатов в консоль."""
    chats = await get_chat_ids_and_names(client)

    for chat_id, chat_name in chats:
        logger.info('%s: %s', chat_id, chat_name)
