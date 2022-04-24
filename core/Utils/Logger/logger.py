import json
from loguru import logger
from django.conf import settings


class Logger(object):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

    FUNCTION_MAP = {
        DEBUG: logger.debug,
        INFO: logger.info,
        WARNING: logger.warning,
        ERROR: logger.error,
    }

    JSON = 'json'
    LOG = 'log'

    def __init__(self,
                 path='',
                 name='',
                 extension='',
                 logger_format='',
                 level='',
                 rotation='',
                 compression='',
                 serialize=True,
                 ):
        self.path = path or settings.CUSTOM_LOGGER_CONFIGS['path']
        self.name = name or settings.CUSTOM_LOGGER_CONFIGS['name']
        self.extension = extension or self.LOG
        self.format = logger_format or settings.CUSTOM_LOGGER_CONFIGS['format']
        self.level = level or self.INFO
        self.rotation = rotation or settings.CUSTOM_LOGGER_CONFIGS['rotation']
        self.compression = compression or settings.CUSTOM_LOGGER_CONFIGS['compression']
        self.serialize = serialize or settings.CUSTOM_LOGGER_CONFIGS['serialize']

        logger.add(f'{self.path}{self.name}.{self.extension}',
                   format=self.format,
                   level=self.level,
                   rotation=self.rotation,
                   compression=self.compression,
                   serialize=self.serialize)

    def log(self, message, level=None):
        if settings.CUSTOM_LOGGER_CONFIGS['active']:
            if self.extension == self.JSON:
                message = json.dumps(message)

            self.FUNCTION_MAP[level or self.level](message)


log = Logger()
