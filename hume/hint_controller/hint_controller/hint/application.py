import threading
import logging

from bottle import run

from .http_server import MyServer
from . import routes  # To load routes
from .settings import hint_req_mod


LOGGER = logging.getLogger(__name__)

server = MyServer(host='localhost', port=8082)


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

    thread = threading.Thread(target=start_http_server)
    thread.start()


def stop():
    """
    Stop the HTTP listener.
    """
    LOGGER.info("device listener stop")
    server.shutdown()


def attach(message_content):
    """
    Sends HINT an attach message.

    :param message_content:
    :return:
    """
    hint_req_mod.attach(message_content)
