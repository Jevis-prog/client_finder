import asyncio

import click
from config import API_HASH, API_ID
from logger import logging
from telethon import TelegramClient
from telethon.sessions import StringSession

from bot.main import routers
from bot.tasks import scheduler, setup_scheduler
from bot.utils.session_manager import load_encrypted_session, save_encrypted_session
from bot.utils.telethone import show_chats


__all__ = ('cli',)
logger = logging.getLogger('cli')


def _init_tg_client(password: str) -> TelegramClient:
    session_str = load_encrypted_session(password)
    client = TelegramClient(StringSession(session_str), api_id=API_ID, api_hash=API_HASH)
    for event, handler in routers:
        client.add_event_handler(handler, event)
    return client


def get_password() -> str:
    """Запрашивает пароль у пользователя."""
    return click.prompt(
        'Введите пароль для доступа к сессии',
        hide_input=True,
    )


@click.group()
def cli() -> None:
    """CLI для управления Telegram ботом."""
    pass


@click.command()
def chats() -> None:
    """Вывести список чатов."""
    password = get_password()
    client = _init_tg_client(password)

    async def main():
        await client.start()
        await show_chats(client)
        await client.disconnect()

    asyncio.run(main())


@click.command()
def run() -> None:
    """Запуск бота."""
    password = get_password()
    client = _init_tg_client(password)

    async def main():
        await client.start()
        setup_scheduler(client)
        scheduler.start()
        await client.run_until_disconnected()
    asyncio.run(main())


@click.command()
def create_session():
    """Создаём и сохраняем первую сессию."""
    password = get_password()
    client = _init_tg_client(password)

    async def main():
        await client.start()
        save_encrypted_session(password, client.session.save())
        await client.disconnect()
    asyncio.run(main())


cli.add_command(run)
cli.add_command(chats)
cli.add_command(create_session)
