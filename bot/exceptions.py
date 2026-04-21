class BotError(Exception):
    """Базовый класс ошибки бота."""

    message = 'Ошибка запроса, повторите снова'
    buttons = None

    def __init__(self, message: str = None, buttons=None, **kwargs):
        if message is not None:
            self.message = message
        if buttons is not None:
            self.buttons = buttons
        super().__init__(**kwargs)


class AiClientError(BotError):
    """Ошибка клиента LLM."""

    message = 'Ошибка работы клиента LLM'


class AiAPIResponseError(BotError):
    """Ошибка ответа LLM."""

    message = 'Ошибка получения ответа от LLM'


class AiAPIRequestError(BotError):
    """Ошибка запроса к LLM."""

    message = 'Ошибка запроса к LLM'


class AiAPIContentError(BotError):
    """Ошибка получения контента от LLM."""

    message = 'Ошибка получения контента LLM'


class AiFormatError(BotError):
    """Ошибка обработки ответа LLM."""

    message = 'Ошибка обработки ответа LLM'


class ScheduleError(BotError):
    """Ошибка работы расписания."""

    message = 'Ошибка работы расписания'


class SessionEncryptingError(BotError):
    """Ошибка декодирования сессии."""

    message = 'Ошибка декодирования сессии'
