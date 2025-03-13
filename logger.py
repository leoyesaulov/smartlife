import logging
from logging import FileHandler

base_logger = logging.getLogger("base")
empty_logger = logging.getLogger("empty")

base_handler = FileHandler(
    filename='.log',
    mode='a',
    encoding='utf-8',
)
empty_handler = FileHandler(
    filename='.log',
    mode='a',
)
base_handler.setLevel(logging.DEBUG)
empty_handler.setLevel(logging.DEBUG)

fmt = logging.Formatter(
    fmt='%(name)s.%(levelname)s at %(asctime)s: %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
)
empty = logging.Formatter(
    fmt=''
)

base_handler.setFormatter(fmt)
empty_handler.setFormatter(empty)

base_logger.addHandler(base_handler)
empty_logger.addHandler(empty_handler)
base_logger.setLevel(logging.DEBUG)
empty_logger.setLevel(logging.DEBUG)

def logInfo(message):
    base_logger.info(message)

def logWarning(message):
    base_logger.warning(message)

def logError(message):
    base_logger.error(message)

def logCritical(message):
    base_logger.critical(message)

def logDebug(message):
    base_logger.debug(message)

def logFatal(message):
    base_logger.fatal(message)

def logEmpty():
    empty_logger.info("")