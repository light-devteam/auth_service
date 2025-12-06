import logging
from functools import cached_property

from src.shared.infrastructure.logger.filters import LoggerFilter
from config import Settings

class LoggerFactory:
    _LOG_FORMAT = '%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_logger(
        self,
        name: str,
        level: int = logging.INFO,
    ) -> logging.Logger:
        log_level = self.__get_logger_level(level)
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        logger.propagate = False
        logger.addFilter(LoggerFilter())
        logger.addHandler(self.file_handler)
        logger.addHandler(self.stream_handler)
        return logger

    @cached_property
    def file_handler(self) -> logging.FileHandler:
        log_level = self.__get_logger_level(logging.WARNING)
        file_handler = logging.FileHandler(self.settings.LOGS_FILE)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(self._LOG_FORMAT))
        return file_handler

    @cached_property
    def stream_handler(self) -> logging.StreamHandler:
        log_level = self.__get_logger_level(logging.INFO)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(logging.Formatter(self._LOG_FORMAT))
        return stream_handler

    def __get_logger_level(self, default_level: int) -> int:
        if self.settings.DEBUG:
            return logging.DEBUG
        return default_level
