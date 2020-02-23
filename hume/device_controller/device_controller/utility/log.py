import logging


TOP_LOGGER_NAME = "device_controller"


def set_up_logging(log_level):
    """
    Sets up the device controller's "root" logger with the starting log level.

    :param log_level: min log level to use for the device controller
    """
    logger = logging.getLogger(TOP_LOGGER_NAME)
    logger.setLevel(log_level)

    handler = logging.StreamHandler()

    formatter = logging.Formatter(fmt="{asctime} {levelname:^8} "
                                      "{module} {message}",
                                  style="{",
                                  datefmt="%d/%m/%Y %H:%M:%S")
    handler.setFormatter(formatter)
    handler.setLevel(log_level)

    logger.addHandler(handler)


def get_root_log_level():
    """
    Returns the "root" logger's effective level, to be able to set sub-logger
    and handler levels appropriately.

    :return: log level of "root" logger
    """
    logger = logging.getLogger(TOP_LOGGER_NAME)
    return logger.getEffectiveLevel()
