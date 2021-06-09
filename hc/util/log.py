import logging
import logging.handlers


LOG_FORMATTER = logging.Formatter(fmt="{asctime} {levelname:^8} "
                                  "HC {name} - {message}",
                                  style="{",
                                  datefmt="%d/%m/%Y %H:%M:%S")
HINT_CONTROLLER_LOG_LEVEL = logging.INFO
HUME_STORAGE_LOG_LEVEL = logging.INFO
RABBITMQ_CLIENT_LOG_LEVEL = logging.INFO

LOGGER = logging.getLogger(__name__)


def set_up_logging():
    """
    Sets up the hc logging for itself and its dependencies
    """

    def set_up_logger_for(name, log_level, handler_type):
        """
        Generic log setup function

        :param name: logger name
        :type log_level: logging.DEBUG for example
        :param handler_type: string for which handler type should be created
        """
        logger = logging.getLogger(name)
        logger.propagate = False
        logger.setLevel(log_level)

        if handler_type == "stream":
            handler = logging.StreamHandler()  # Print logging messages
        # elif ...
        handler.setFormatter(LOG_FORMATTER)

        handler.setLevel(log_level)
        logger.addHandler(handler)

    # SET UP LOGGERS
    set_up_logger_for(None,  # Root logger
                      HINT_CONTROLLER_LOG_LEVEL,
                      "stream")
    set_up_logger_for("hume_storage",
                      HUME_STORAGE_LOG_LEVEL,
                      "stream")
    set_up_logger_for("rabbitmq_client",
                      RABBITMQ_CLIENT_LOG_LEVEL,
                      "stream")

    # Set up monitor log queue
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(LOG_FORMATTER)

    # Disable pika logging
    pika_logger = logging.getLogger("pika")
    pika_logger.propagate = False


def stop_logging():
    """
    Stops logging processed gracefully.
    """
    LOGGER.info("stopping logging")


def get_root_log_level():
    """
    Returns the "root" logger's effective level, to be able to set sub-logger
    and handler levels appropriately.

    :return: log level of "root" logger
    """
    logger = logging.getLogger(TOP_LOGGER_NAME)
    return logger.getEffectiveLevel()
