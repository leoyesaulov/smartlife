import logging
from logging import FileHandler

__base_logger = logging.getLogger("base")

__base_handler = FileHandler(
    filename='.log',
    mode='a',
    encoding='utf-8',
)

__base_handler.setLevel(logging.DEBUG)

__fmt = logging.Formatter(
    fmt='%(name)s.%(levelname)s at %(asctime)s: %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
)

__base_handler.setFormatter(__fmt)

__base_logger.addHandler(__base_handler)
__base_logger.setLevel(logging.DEBUG)


def nothing(str):
    return


# def log(type, message, func):
#     __base_logger.__getattribute__(type).__call__(message)
#     __base_logger.log(type, message)

def logInfo(message, func=nothing):
    func(message)
    __base_logger.info(message)


def logWarning(message, func=nothing):
    func(message)
    __base_logger.warning(message)


def logError(message, func=nothing):
    func(message)
    __base_logger.error(message)


def logCritical(message, func=nothing):
    func(message)
    __base_logger.critical(message)


def logDebug(message, func=nothing):
    func(message)
    __base_logger.debug(message)


def logFatal(message, func=nothing):
    func(message)
    __base_logger.fatal(message)
