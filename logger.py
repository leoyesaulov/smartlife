import logging

logging.basicConfig(
    format='%(name)s.%(levelname)s at %(asctime)s: %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
    filename='.log',
    encoding='utf-8',
    filemode='a',
    level=logging.INFO
)

def logInfo(message):
    logging.info(message)

def logWarning(message):
    logging.warning(message)

def logError(message):
    logging.error(message)

def logCritical(message):
    logging.critical(message)

def logDebug(message):
    logging.debug(message)

def logFatal(message):
    logging.fatal(message)