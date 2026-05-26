import logging

def setup_logging(level: str = "INFO"):
    level_dict = {"DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL}
    logging.basicConfig(level = level_dict[level.upper()],
            format = "[%(name)s] [%(levelname)s]: %(message)s")

def get_logger(name: str):
    short_name = name.split('.')[-1]
    return logging.getLogger(short_name)
