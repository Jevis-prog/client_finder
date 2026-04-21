from enum import StrEnum


class ProcessingStatus(StrEnum):
    """Статусы для обработки комментариев нейросетью."""

    PENDING = 'pending'
    ANALYZED = 'analyzed'
    FAILED = 'failed'
    BROKEN = 'broken'


class MessageRole(StrEnum):
    """Общие типы для LLM."""

    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'
