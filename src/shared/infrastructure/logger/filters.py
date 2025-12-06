from logging import Filter, LogRecord

class LoggerFilter(Filter):
    COLOR = {
        'DEBUG': 'GREEN',
        'INFO': 'GREEN',
        'WARNING': 'YELLOW',
        'ERROR': 'RED',
        'CRITICAL': 'RED',
    }

    def filter(self, record: LogRecord) -> bool:
        record.color = LoggerFilter.COLOR[record.levelname]
        return True
