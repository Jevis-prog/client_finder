from config import CHATS
from telethon import events
from telethon.events import NewMessage

from bot.uow.sql import SQLUoW
from bot.utils.telethone import get_chat_data


async def message_listener(event: NewMessage.Event) -> None:
    """Обработчик слушающий сообщения в чатах."""
    msg_info = await get_chat_data(event)
    sender = await event.get_sender()

    async with SQLUoW() as uow:
        user = await uow.user_repo.get_or_create(
            external_id=msg_info.sender_id, username=sender.username,
        )
        chat = await uow.chat_repo.get_or_create(
            external_id=msg_info.chat_id,
            chat_title=msg_info.chat_title,
        )
        await uow.message_repo.save_message_to_db(
            sender_id=user.id,
            chat_id=chat.id,
            external_id=msg_info.external_id,
            message_text=msg_info.message_text,
            processing_status=msg_info.processing_status,
        )


routers = [
    (events.NewMessage(chats=CHATS), message_listener),
]
