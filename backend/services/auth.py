import secrets
from datetime import datetime, timedelta

from config import TOKEN_EXPIRE_MINUTES, TOKEN_LENGTH
from bot.db.models import AdminUserModel
from bot.uow.sql import SQLUoW


def generate_token(length: int = TOKEN_LENGTH) -> str:
    """Генерация токена указанной длины."""
    bytes_count = (length * 3) // 4 + 1
    token_bytes = secrets.token_bytes(bytes_count)
    return secrets.token_urlsafe(len(token_bytes))[:length]


async def authenticate_user(username: str, password_hash: str) -> AdminUserModel | None:
    """Аутентификация пользователя админки."""
    async with SQLUoW() as uow:
        user = await uow.admin_user_repo.get(username=username)
        if user and user.password_hash == password_hash:
            return user
        return None


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
