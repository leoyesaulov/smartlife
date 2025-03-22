import logging
from logging import FileHandler

__base_logger = logging.getLogger("base")
__empty_logger = logging.getLogger("empty")

__base_handler = FileHandler(
    filename='.log',
    mode='a',
    encoding='utf-8',
)
__empty_handler = FileHandler(
    filename='.log',
    mode='a',
)
__base_handler.setLevel(logging.DEBUG)
__empty_handler.setLevel(logging.DEBUG)

__fmt = logging.Formatter(
    fmt='%(name)s.%(levelname)s at %(asctime)s: %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
)
__empty = logging.Formatter(
    fmt=''
)

__base_handler.setFormatter(__fmt)
__empty_handler.setFormatter(__empty)

__base_logger.addHandler(__base_handler)
__empty_logger.addHandler(__empty_handler)
__base_logger.setLevel(logging.DEBUG)
__empty_logger.setLevel(logging.DEBUG)

def logInfo(message):
    __base_logger.info(message)

def logWarning(message):
    __base_logger.warning(message)

def logError(message):
    __base_logger.error(message)

def logCritical(message):
    __base_logger.critical(message)

def logDebug(message):
    __base_logger.debug(message)

def logFatal(message):
    __base_logger.fatal(message)

def logEmpty():
    __empty_logger.info("")