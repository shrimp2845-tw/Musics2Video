import logging

def setup_logging(level: str = "INFO"):
    """
    Initializes and configures global logging settings.

    Args:
        level (str): The desired log level string (e.g., 'DEBUG', 'INFO').
    """
    level_dict = {"DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL}
    logging.basicConfig(level = level_dict[level.upper()],
            format = "[%(name)s] [%(levelname)s]: %(message)s")

def get_logger(name: str) -> logging.Logger:
    """
    Retrieves a logger instance named after the last module identifier component.

    Args:
        name (str): Full module name (typically __name__).

    Returns:
        logging.Logger: Parsed short-named Logger instance.
    """
    short_name = name.split('.')[-1]
    return logging.getLogger(short_name)
