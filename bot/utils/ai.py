import json
import re

from logger import logging

from bot.exceptions import AiFormatError
from bot.utils.schemas import MessageAnalysis


logger = logging.getLogger('ai_service')


def content_formater(content: str) -> list[MessageAnalysis]:
    """Перерабатывает ответ нейронки в нужный формат."""
    content = content.strip()
    if content.startswith('```'):
        content = re.sub(r'^```[a-zA-Z]*\n', '', content)
        content = re.sub(r'\n```$', '', content)

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        logger.error(f'Failed to parse OpenAI response as JSON. Content: {content}')
        raise

    # Преобразуем словари в MessageAnalysis
    analysis_list: list[MessageAnalysis] = []
    for item in data:
        try:
            msg = MessageAnalysis(
                sender_id=str(item.get('sender_id', '')),
                message_text=str(item.get('message_text', '')),
                id=int(item['message_id']),
            )
            msg.set_analysis_result(
                is_lead=bool(item['is_lead']),
                reason=str(item['reason']),
            )
            analysis_list.append(msg)
        except KeyError as e:
            logger.error(f'Missing key in item: {item}, Error: {e}')
            raise AiFormatError(message=f'Отсутствует ключ {e.args[0]} в ответе LLM') from e
        except ValueError as e:
            logger.error(f'Invalid value in item: {item}, Error: {e}')
            raise AiFormatError(message='Ошибка преобразования данных LLM') from e
        except Exception as e:
            logger.error(f'Unexpected error processing item: {item}, Error: {e}')
            raise AiFormatError(message='Неожиданная ошибка при обработке ответа LLM') from e

    return analysis_list
