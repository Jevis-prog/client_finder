from abc import ABC, abstractmethod
from typing import Any, Type

from logger import logging
from openai import APIConnectionError, APIError, AsyncOpenAI, BadRequestError, RateLimitError
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from bot.const import MessageRole
from bot.exceptions import AiAPIContentError, AiAPIRequestError, AiAPIResponseError
from bot.utils.ai import content_formater
from bot.utils.schemas import MessageAnalysis


logger = logging.getLogger('ai_service')

PROMPT_FILE = 'bot/prompts/analyze_messages.txt'

with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
    PROMPT_TEMPLATE = f.read()


class LLMMessage:
    """Универсальное сообщение для LLM."""

    def __init__(self, role: MessageRole, content: str):
        self.role = role
        self.content = content


class LLMClientProtocol(ABC):
    """Абстрактный класс для клиентов LLM."""

    @abstractmethod
    async def send_request(
        self,
        messages: list[LLMMessage],
    ) -> list[MessageAnalysis]:
        """Отправка запроса к LLM."""
        pass


class OpenAIClientAdapter(LLMClientProtocol):
    """Адаптер для OpenAI API."""

    def __init__(self, api_key: str, base_url: str, model: str):
        self.model: str = model
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    @staticmethod
    def _to_openai_messages(messages: list[LLMMessage]) -> list[Any]:
        """Преобразует внутренние LLMMessage в формат OpenAI SDK."""
        result = []
        for m in messages:
            if m.role == MessageRole.SYSTEM:
                result.append(ChatCompletionSystemMessageParam(role='system', content=m.content))
            elif m.role == MessageRole.USER:
                result.append(ChatCompletionUserMessageParam(role='user', content=m.content))
            elif m.role == MessageRole.ASSISTANT:
                result.append(
                    ChatCompletionAssistantMessageParam(role='assistant', content=m.content),
                )
        return result

    async def send_request(
        self,
        messages: list[LLMMessage],
    ) -> list[MessageAnalysis]:
        """Отправляет запрос LLM и возвращает список MessageAnalysis."""
        logger.info(f'Sending request to OpenAI model "{self.model}" with {len(messages)} messages')
        try:
            resp = await self.client.chat.completions.create(
                model=self.model,
                messages=self._to_openai_messages(messages),
            )
        except (APIError, APIConnectionError, RateLimitError, BadRequestError) as e:
            logger.error(f'OpenAI API exception: {e}')
            raise AiAPIRequestError() from e

        logger.debug(f'Raw OpenAI response: {resp}')

        if not resp.choices:
            logger.error('No choices in response')
            raise AiAPIContentError()

        raw_content = resp.choices[0].message.content
        if not raw_content:
            raise AiAPIContentError()

        return content_formater(raw_content)


class LLM:
    """Обертка над клиентом LLM для отправки сообщений."""

    def __init__(
        self,
        client: LLMClientProtocol,
        model_name: str | None = None,
    ):
        self.model = model_name
        self.client = client

    async def send(self, request: list[LLMMessage]) -> list[MessageAnalysis]:
        """Отправляет запрос LLM и возвращает ответ."""
        try:
            return await self.client.send_request(
                messages=request,
            )
        except AiAPIResponseError as e:
            raise AiAPIResponseError() from e
        except Exception as err:
            logger.exception(f'Unexpected error in LLM.send(): {repr(err)}')
            raise


class AIMessageHandler:
    """Подготовка промпта и постобработка ответа модели."""

    @staticmethod
    def generate_prompt(messages: list[MessageAnalysis]) -> str:
        """Генерирует промпт на основе шаблона."""
        messages_str = '\n\n'.join(
            (
                f'Chat_id: {msg.chat_id}\n'
                f'Sender: {msg.sender_id}\n'
                f'Message ID: {msg.id}\n'
                f'Message text: {msg.message_text}'
            )
            for msg in messages
        )
        return PROMPT_TEMPLATE.format(messages=messages_str)

    def preprocessing(self, messages: list[MessageAnalysis]) -> list[LLMMessage]:
        """Подготавливает запрос к LLM."""
        return [
            LLMMessage(
                role=MessageRole.SYSTEM,
                content='You are a JSON API. Respond ONLY with valid JSON.',
            ),
            LLMMessage(
                role=MessageRole.USER,
                content=self.generate_prompt(messages),
            ),
        ]


class AIService:
    """Фасад для работы с LLM: подготовка, отправка и разбор ответа."""

    def __init__(self, api_key: str, base_url: str, model: str, client: Type[LLMClientProtocol]):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.handler = AIMessageHandler()
        self.client = client(self.api_key, self.base_url, self.model)  # type: ignore
        self.llm = LLM(client=self.client)

    async def analyze_messages(self, messages: list[MessageAnalysis])\
            -> dict[int, MessageAnalysis]:
        """Анализирует сообщения и возвращает маппинг по message_id."""
        logger.info(f'Analyzing {len(messages)} messages via AIService')
        request = self.handler.preprocessing(messages)
        logger.debug(f'Prepared LLM request: {request}')
        result = await self.llm.send(request)
        logger.debug(f'AI analysis result: {result}')

        response_map: dict[int, MessageAnalysis] = {}

        for item in result:
            if item.is_analyzed:
                msg_id = int(item.id)
                response_map[msg_id] = item
            else:
                continue

        return response_map
