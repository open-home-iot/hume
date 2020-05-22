import threading
import logging

from bottle import run
from . import routes  # To load routes
from .http_server import MyServer

LOGGER = logging.getLogger(__name__)

server = MyServer(host='localhost', port=8081)


def start():
    """
    Starts up the HTTP listener.
    """

    def start_http_server():
        """
        Starts an HTTP server locally on port 8081.
        """
        run(server=server)  # Blocks!

    LOGGER.info("device listener start")

    # TODO well, what will be used to communicate with devices?
    thread = threading.Thread(target=start_http_server)
    thread.start()


def stop():
    """
    Stop the HTTP listener.
    """
    LOGGER.info("device listener stop")
    server.shutdown()


def send_device_message(message):
    """
    Sends a device a message.

    :param message:
    :return:
    """
    pass
