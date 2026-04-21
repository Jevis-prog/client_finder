import logging
import logging.config
from pathlib import Path


LOG_PATH_DIR = Path('logs')
LOG_PATH_DIR.mkdir(exist_ok=True)

LOGGER_LEVEL = 'DEBUG'

LOGGER_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_formatter': {
            'format': (
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                ' - %(filename)s - %(lineno)s - %(funcName)s'
            ),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': LOGGER_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'fileTaskHandler': {
            'level': LOGGER_LEVEL,
            'class': 'logging.FileHandler',
            'filename': (LOG_PATH_DIR / 'tasks.log').as_posix(),
            'formatter': 'main_formatter',
        },
        'fileAIHandler': {
            'level': LOGGER_LEVEL,
            'class': 'logging.FileHandler',
            'filename': (LOG_PATH_DIR / 'ai.log').as_posix(),
            'formatter': 'main_formatter',
        },
        'fileTgHandler': {
            'level': LOGGER_LEVEL,
            'class': 'logging.FileHandler',
            'filename': (LOG_PATH_DIR / 'tg.log').as_posix(),
            'formatter': 'main_formatter',
        },
        'fileCliHandler': {
            'level': LOGGER_LEVEL,
            'class': 'logging.FileHandler',
            'filename': (LOG_PATH_DIR / 'cli.log').as_posix(),
            'formatter': 'main_formatter',
        },
    },
    'loggers': {
        'tasks': {
            'handlers': ['console', 'fileTaskHandler'],
            'level': LOGGER_LEVEL,
        },
        'ai_service': {
            'handlers': ['console', 'fileAIHandler'],
            'level': LOGGER_LEVEL,
        },
        'tg_service': {
            'handlers': ['console', 'fileTaskHandler'],
            'level': LOGGER_LEVEL,
        },
        'tgbot_app': {
            'handlers': ['console', 'fileTgHandler'],
            'level': LOGGER_LEVEL,
        },
        'cli': {
            'handlers': ['console', 'fileCliHandler'],
            'level': LOGGER_LEVEL,
        },
    },
}

logging.config.dictConfig(LOGGER_CONFIG)
