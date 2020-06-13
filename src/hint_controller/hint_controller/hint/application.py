import threading
import logging

from bottle import run

from .http_server import MyServer
from .settings import req_mod
from . import routes  # To load routes


LOGGER = logging.getLogger(__name__)

server = MyServer(host='localhost', port=8082)


def start():
    """
    Starts up the HTTP listener.
    """
    LOGGER.info("hint start")

    def start_http_server():
        """
        Starts an HTTP server locally on port 8082. This sever listens for
        requests sent from the cloud (HINT).
        """
        run(server=server)  # Blocks!

    thread = threading.Thread(target=start_http_server)
    thread.start()


def stop():
    """
    Stop the HTTP listener.
    """
    LOGGER.info("hint stop")

    server.shutdown()


def attach(message_content):
    """
    Sends HINT an attach message.

    :param message_content:
    :return:
    """
    LOGGER.info("sending attach to HINT")

    req_mod().attach(message_content)


def device_event(message_content):
    """
    Sends HINT a device event message

    :param message_content:
    :return:
    """
    LOGGER.info("sending device event to HINT")

    req_mod().device_event(message_content)


def sub_device_event(message_content):
    """
    Sends HINT a sub device event message

    :param message_content:
    :return:
    """
    LOGGER.info("sending sub device event to HINT")

    req_mod().sub_device_event(message_content)

