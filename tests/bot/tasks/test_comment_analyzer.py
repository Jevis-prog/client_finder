import pytest

from bot.utils.schemas import MessageAnalysis
from bot.utils.tasks import batch_generator


@pytest.fixture
def messages() -> list[MessageAnalysis]:
    """Фикстура для тестовых сообщений."""
    return [
        MessageAnalysis(sender_id='1', message_text='Short message', id=1),
        MessageAnalysis(sender_id='2', message_text='Another short message', id=2),
        MessageAnalysis(sender_id='3', message_text='Third short message', id=3),
    ]


def test_batch_generator_single_chunk(messages):
    """Тестируем создание одного чанка при большом batch_size."""
    chunks = list(batch_generator(messages, batch_size=1000))

    # Должен быть один чанк
    assert len(chunks) == 1

    # В чанке должны быть все сообщения
    assert len(chunks[0]) == len(messages)
    assert chunks[0] == messages


def test_batch_generator_multiple_chunks(messages):
    """Тестируем создание нескольких чанков при маленьком batch_size."""
    chunks = list(batch_generator(messages, batch_size=2))

    # Должно быть несколько чанков
    assert len(chunks) > 1

    # Все сообщения должны быть сохранены
    flattened = [msg for chunk in chunks for msg in chunk]
    assert len(flattened) == len(messages)
    assert flattened == messages

    # Каждый чанк должен содержать MessageForAnalysis
    for chunk in chunks:
        assert isinstance(chunk, list)
        assert all(isinstance(msg, MessageAnalysis) for msg in chunk)
