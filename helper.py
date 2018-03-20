import logging

import settings

"""
Helper module for socknet library
"""


def get_logger(name, logger_logging_level=logging.DEBUG, stream_logging_level=logging.DEBUG):
    """
    Create a logger (or simply fetch if one already exists) with desired logging levels.
    :param name: Name of logger (str)
    :param logger_logging_level: Logger logging level [logging.DEBUG [..INFO, WARNING, ERROR, CRITICAL]] (logging.*)
    :param stream_logging_level: Stream logging level [logging.DEBUG [..INFO, WARNING, ERROR, CRITICAL]] (logging.*)
    :return: New or existing logger (Logger object)
    """
    base_logger = logging.getLogger(name)
    base_logger.setLevel(logger_logging_level)
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(stream_logging_level)

    base_logger.handlers = []
    base_logger.addHandler(stream_handler)

    return base_logger


logger = get_logger(settings.LOGGER_NAME)


def is_num(text):
    """
    Check if given text is a number (int or float)
    :param text: Text (str)
    :return: Whether number (bool)
    """
    try:
        _ = float(text) if '.' in text else int(text)
        return True
    except ValueError:
        return False
