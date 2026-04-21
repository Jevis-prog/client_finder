from os import getenv
from dotenv import load_dotenv

load_dotenv()


def env_int(param_name: str, default: int | None = None) -> int | None:
    """Функция, преобразующая переменную окружения в целочисленное значение."""
    value = getenv(param_name, '').strip()
    try:
        return int(value)
    except ValueError:
        return default


def env_list(param_name: str, default: str = '', separator: str = ',') -> list[int]:
    """Функция, преобразующая переменную окружения в список целых чисел."""
    value = getenv(param_name, default)
    tokens = [x.strip() for x in value.strip().split(separator) if x.strip()]
    result: list[int] = []
    for token in tokens:
        try:
            result.append(int(token))
        except ValueError:
            continue
    return result


def env_str_list(param_name: str, default: list[str] | None = None, separator: str = ',') -> list[str]:
    """Функция, преобразующая переменную окружения в список строк."""
    value = getenv(param_name)
    if value is None:
        return default or []
    return [x.strip() for x in value.strip().split(separator) if x.strip()]


DB_TYPE = 'postgresql'
DB_DRIVER = 'asyncpg'
DB_USER = getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = getenv('POSTGRES_PASSWORD', 'postgres')
DB_HOST = getenv('PG_HOST', 'localhost')
DB_PORT = env_int('PG_PORT', 5432)
DB_NAME = getenv('PG_DB_NAME', 'tg_bot_db')

DB_STR = f'{DB_TYPE}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

DB_COMMENTS_TIMEOUT = env_int('DB_COMMENTS_TIMEOUT', 300)
DB_FAILED_COMMENTS_TIMEOUT = env_int('B_FAILED_COMMENTS_TIMEOUT', 350)

ENCRYPT_SESSION_FILE = getenv(
    'ENCRYPT_SESSION_FILE',
    'sessions/bot_session.enc',
)
API_ID = env_int('API_ID', 0)
API_HASH = getenv('API_HASH')
TARGET_CHAT_ID = env_int('TARGET_CHAT_ID', 0)
CHATS = env_list('CHATS')
DEEPSEEK_API_KEY = getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = getenv('DEEPSEEK_API_URL')
OPEN_ROUTER_API_KEY = getenv('OPEN_ROUTER_API_KEY')
OPEN_ROUTER_API_URL = getenv('OPEN_ROUTER_API_URL')
DEEPSEEK_MODEL = getenv('DEEPSEEK_MODEL')

FASTAPI_ALLOW_ORIGINS = env_str_list('FASTAPI_ALLOW_ORIGINS', [])
FASTAPI_COOKIE_SECURE = getenv('COOKIE_SECURE_ENABLED', 'True').lower() == 'true'
SESSION_COOKIE_NAME = getenv('SESSION_COOKIE_NAME', 'access_token')
ADMIN_BOOTSTRAP_TOKEN = getenv('ADMIN_BOOTSTRAP_TOKEN')
TOKEN_EXPIRE_MINUTES = env_int('TOKEN_EXPIRE_MINUTES', 60) or 60
TOKEN_LENGTH = env_int('TOKEN_LENGTH', 48) or 48
