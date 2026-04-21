import math
from dataclasses import asdict, dataclass
from enum import StrEnum

from pydantic import BaseModel


RUSSIANS_LETTERS_TOKENS = 1.33
ONE_TOKEN = 4


class MessageForAnalyzeStatus(StrEnum):
    """Статусы обработки сообщений."""

    SUCCESS = 'success'
    FAILED = 'failed'


class AnalysisResult(BaseModel):
    """Результат анализа сообщения AI с валидацией."""

    is_lead: bool
    reason: str


@dataclass
class MessageAnalysis:
    """Сообщение для анализа с результатами."""

    sender_id: str
    message_text: str
    id: int
    sender_username: str | None = None
    message_id: str | None = None
    chat_id: str | None = None
    chat_title: str | None = None
    result: AnalysisResult | None = None
    status: MessageForAnalyzeStatus = MessageForAnalyzeStatus.FAILED

    def dict(self) -> dict[str, str]:
        """Десериализация данных."""
        return asdict(self)

    @property
    def length(self) -> int:
        """Замеряет количество токенов в сообщении."""
        return math.ceil((len(self.sender_id) + len(self.message_text))
                         * RUSSIANS_LETTERS_TOKENS / ONE_TOKEN)

    @property
    def is_analyzed(self) -> bool:
        """Проверяет, проанализировано ли сообщение."""
        return self.result is not None

    def set_analysis_result(self, is_lead: bool, reason: str) -> None:
        """Устанавливает результат анализа."""
        self.result = AnalysisResult(is_lead=is_lead, reason=reason)
