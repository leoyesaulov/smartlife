from logging import FileHandler, getLogger, INFO, Formatter

__base_logger = getLogger("base")

__base_handler = FileHandler(
    filename='.log',
    mode='a',
    encoding='utf-8',
)

__base_handler.setLevel(INFO)

__fmt = Formatter(
    fmt='%(name)s.%(levelname)s at %(asctime)s: %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
)

__base_handler.setFormatter(__fmt)

__base_logger.addHandler(__base_handler)
__base_logger.setLevel(INFO)

levels = {
    "notset": 0,
    "debug": 10,
    "info": 20,
    "warning": 30,
    "error": 40,
    "critical": 50
}


def log(message:str, type:str, func=None) -> None:
    if func: func(message)
    __base_logger.log(level=levels[type], msg=message)