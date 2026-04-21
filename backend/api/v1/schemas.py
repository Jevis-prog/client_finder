from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    """Запрос на регистрацию пользователя админки."""

    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserLogin(BaseModel):
    """Модель аутентификации."""

    username: str
    password_hash: str


class CurrentUserOut(BaseModel):
    """Текущий пользователь админки."""

    id: int
    username: str


class LeadOut(BaseModel):
    """Сообщение-лид для админки."""

    id: int
    external_id: int
    sender_id: int
    chat_id: int
    message_text: str
    is_lead: bool | None
    reason: str | None
    processing_status: str
    username: str | None = None
    chat_title: str | None = None
