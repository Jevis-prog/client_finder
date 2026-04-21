import asyncio
import base64
import logging
from hashlib import sha256

from cryptography.fernet import Fernet
from telethon import TelegramClient
from telethon.sessions import StringSession


logger = logging.getLogger('tg_service')

API_ID = ''  # Vault
API_HASH = ''  # Vault

ENCRYPT_SESSION_FILE = 'bot_session.enc'


def generate_key_from_password(password: str) -> bytes:
    """Генерирует ключ из пароля."""
    return base64.urlsafe_b64encode(sha256(password.encode()).digest())


def encrypt_and_save_session(password: str, session) -> None:
    """Шифрует и сохраняет сессию."""
    key = generate_key_from_password(password)
    fernet = Fernet(key)
    session_bytes = session.encode('utf-8')
    encrypted_data = fernet.encrypt(session_bytes)
    with open(ENCRYPT_SESSION_FILE, 'wb') as f:
        f.write(encrypted_data)
    logger.info('Сессия зашифрована и сохранена.')


client = TelegramClient(StringSession(None), api_id=API_ID, api_hash=API_HASH)


if __name__ == '__main__':
    password = input('Введите пароль: ')

    async def main():
        """Запуск клиента и сохранение сессии."""
        await client.start()
        encrypt_and_save_session(password, client.session.save())
        await client.disconnect()
    asyncio.run(main())
