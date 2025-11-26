from logging import FileHandler, getLogger, INFO, Formatter
from warnings import DeprecatedWarning, warn

fmt = Formatter(
    fmt='%(name)s.%(levelname)s at %(asctime)s: %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
)

base_handler = FileHandler(
    filename='.log',
    mode='a',
    encoding='utf-8',
)
base_handler.setLevel(INFO)
base_handler.setFormatter(fmt)

base_logger = getLogger("base")
base_logger.addHandler(base_handler)
base_logger.setLevel(INFO)

levels = {
    "notset": 0,
    "debug": 10,
    "info": 20,
    "warning": 30,
    "error": 40,
    "critical": 50
}

def log(message:str, type:str, func=None) -> None:
    """
    Logs the <message> with <type> level into a ./.log file
    """
    if func: 
        func(message)
        warn("Usage of argument func is deprecated and will be removed in the future, use a separate function outside of logging", DeprecatedWarning)
    base_logger.log(level=levels[type], msg=message)
