from sqlalchemy import delete, select

from bot.db.models import AuthTokenModel
from bot.db.repository.base import BaseRepository


class AuthRepository(BaseRepository):
    """Репозиторий токенов админки."""

    async def create_token(self, user_id: int, token: str, expires_at) -> AuthTokenModel:
        auth_token = AuthTokenModel(user_id=user_id, token=token, expires_at=expires_at)
        self.session.add(auth_token)
        return auth_token

    async def get_token(self, token: str) -> AuthTokenModel | None:
        stmt = select(AuthTokenModel).where(AuthTokenModel.token == token)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_token(self, token: str) -> bool:
        stmt = (
            delete(AuthTokenModel)
            .where(AuthTokenModel.token == token)
            .returning(AuthTokenModel.id)
        )
        result = await self.session.execute(stmt)
        return bool(result.one_or_none())
