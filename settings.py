import environ
import os
import sys
from pathlib import Path

# default env vals
env = environ.Env(
    DEBUG = (bool, False),
    LOG_FILE = (str, "logs/status.log"),
    LOG_LVL = (str, 'INFO'),

    GMAIL_CREDENTIALS_FILE = (str, ''),
    GMAIL_ACCESS_TOKEN_FILE = (str, ''),
    TRASH_LABEL = (str, ''),
    SCOPES = (list, []),

    BOT_TOKEN = (str, ''),
    CHAT_IDS = (list, []),
    CHAT_PW = (str, '')
)

BASE_DIR = Path(__file__).resolve()
env.read_env(os.path.join(BASE_DIR, '.env','.env'))


# GMAIL credentials + settings
GMAIL_CREDENTIALS_FILE = env.str('GMAIL_CREDENTIALS_FILE')
GMAIL_ACCESS_TOKEN_FILE = env.str('GMAIL_ACCESS_TOKEN_FILE')

TRASH_LABEL = env.str('TRASH_LABEL')
SCOPES = env.list('SCOPES')


# OpenAI settings
# TODO

# Bot settings
BOT_TOKEN = env.str('BOT_TOKEN')
CHAT_IDS = env.list('CHAT_IDS')
CHAT_PW = env.str('CHAT_PW')



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} | {message}',
            'style': '{'
        },
        'minimal': {
            'format': '[%(levelname)s] %(module)s: %(message)s'
        },
        'formatter_json':{
            'format': '%(levelname)s %(asctime)s %(module)s %(process)s %(thread)s %(message)s',
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'minimal'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': env.str('LOG_FILE'),
            'formatter': 'formatter_json',
            'maxBytes': 5270000,
            'backupCount': 1
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING'
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': env.str('LOG_LVL'),
            'propagate': False
        }
    }
}