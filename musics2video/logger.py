import logging

def setup_logging(level: str = "INFO", name: str = 'undifined'):
    level_dict = {"DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL}
    logging.basicConfig(level = level_dict[level.upper()],
            format = f"[{name}] [%(levelname)s]: %(message)s")

def get_logger(name: str):
    return logging.getLogger(name)
