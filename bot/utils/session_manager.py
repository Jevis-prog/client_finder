import base64
import os
from hashlib import sha256

from config import ENCRYPT_SESSION_FILE
from cryptography.fernet import Fernet, InvalidToken
from logger import logging

from bot.exceptions import SessionEncryptingError


logger = logging.getLogger('tg_service')


def generate_key_from_password(password: str) -> bytes:
    """Генерирует ключ из пароля."""
    return base64.urlsafe_b64encode(sha256(password.encode()).digest())


def load_encrypted_session(password: str):
    """Загружает и расшифровывает сессию."""
    key = generate_key_from_password(password)
    fernet = Fernet(key)

    if not os.path.exists(ENCRYPT_SESSION_FILE):
        return
    with open(ENCRYPT_SESSION_FILE, 'rb') as f:
        encrypted_data = f.read()
    try:
        session_data = fernet.decrypt(encrypted_data)
        logger.info('Сессия успешно расшифрована.')
        return session_data.decode('utf-8')
    except InvalidToken:
        raise SessionEncryptingError


def save_encrypted_session(password: str, session) -> None:
    """Шифрует и сохраняет сессию."""
    key = generate_key_from_password(password)
    fernet = Fernet(key)
    session_bytes = session.encode('utf-8')
    encrypted_data = fernet.encrypt(session_bytes)
    with open(ENCRYPT_SESSION_FILE, 'wb') as f:
        f.write(encrypted_data)
    logger.info('Сессия зашифрована и сохранена.')
