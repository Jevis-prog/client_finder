from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    """Модель аутентификации."""

    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


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


class StatsOut(BaseModel):
    """Сводная статистика для админки."""

    total_messages: int
    processed_messages: int
    total_leads: int
    valid_leads: int
    processed_last_day: int
    processed_last_hour: int
