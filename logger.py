from logging import FileHandler, getLogger, INFO, Formatter

base_logger = getLogger("base")

base_handler = FileHandler(
    filename='.log',
    mode='a',
    encoding='utf-8',
)

base_handler.setLevel(INFO)

fmt = Formatter(
    fmt='%(name)s.%(levelname)s at %(asctime)s: %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
)

base_handler.setFormatter(fmt)

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
    if func: func(message)
    base_logger.log(level=levels[type], msg=message)