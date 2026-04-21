import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta

from config import TOKEN_EXPIRE_MINUTES, TOKEN_LENGTH
from bot.db.models import AdminUserModel
from bot.uow.sql import SQLUoW


SCRYPT_PREFIX = 'scrypt'
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_SALT_SIZE = 16


def generate_token(length: int = TOKEN_LENGTH) -> str:
    """Генерация токена указанной длины."""
    bytes_count = (length * 3) // 4 + 1
    token_bytes = secrets.token_bytes(bytes_count)
    return secrets.token_urlsafe(len(token_bytes))[:length]


def hash_password(password: str) -> str:
    """Создание salted scrypt-хеша пароля."""
    salt = secrets.token_bytes(SCRYPT_SALT_SIZE)
    password_hash = hashlib.scrypt(
        password.encode('utf-8'),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
    )
    salt_b64 = base64.b64encode(salt).decode('ascii')
    hash_b64 = base64.b64encode(password_hash).decode('ascii')
    return f'{SCRYPT_PREFIX}${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}${salt_b64}${hash_b64}'


def _verify_scrypt_password(password: str, password_hash: str) -> bool:
    try:
        prefix, n, r, p, salt_b64, hash_b64 = password_hash.split('$', 5)
    except ValueError:
        return False

    if prefix != SCRYPT_PREFIX:
        return False

    salt = base64.b64decode(salt_b64.encode('ascii'))
    expected_hash = base64.b64decode(hash_b64.encode('ascii'))
    actual_hash = hashlib.scrypt(
        password.encode('utf-8'),
        salt=salt,
        n=int(n),
        r=int(r),
        p=int(p),
    )
    return hmac.compare_digest(actual_hash, expected_hash)


def verify_password(password: str, password_hash: str) -> tuple[bool, bool]:
    """
    Проверка пароля.

    Возвращает:
    - признак успешной проверки
    - признак того, что хеш устарел и его нужно обновить
    """
    if password_hash.startswith(f'{SCRYPT_PREFIX}$'):
        return _verify_scrypt_password(password, password_hash), False

    legacy_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hmac.compare_digest(legacy_hash, password_hash), True


async def authenticate_user(username: str, password: str) -> AdminUserModel | None:
    """Аутентификация пользователя админки."""
    async with SQLUoW() as uow:
        user = await uow.admin_user_repo.get(username=username)
        if user is None:
            return None

        is_valid, needs_rehash = verify_password(password, user.password_hash)
        if not is_valid:
            return None

        if needs_rehash:
            await uow.admin_user_repo.update(user.id, password_hash=hash_password(password))
            await uow.commit()

        return user


async def create_token_for_user(
    user_id: int,
    expire_minutes: int = TOKEN_EXPIRE_MINUTES,
) -> str:
    """Создание токена для пользователя."""
    token = generate_token(TOKEN_LENGTH)
    expires_at = datetime.now() + timedelta(minutes=expire_minutes)

    async with SQLUoW() as uow:
        await uow.auth_token_repo.create_token(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )

    return token


async def get_user_by_token(token: str | None) -> AdminUserModel | None:
    """Получение пользователя по токену."""
    if not token:
        return None

    async with SQLUoW() as uow:
        token_obj = await uow.auth_token_repo.get_token(token)
        if token_obj is None or token_obj.expires_at < datetime.now():
            return None

        return await uow.admin_user_repo.get(user_id=token_obj.user_id)


async def delete_token(token: str) -> bool:
    """Выход из системы."""
    async with SQLUoW() as uow:
        return await uow.auth_token_repo.delete_token(token)
