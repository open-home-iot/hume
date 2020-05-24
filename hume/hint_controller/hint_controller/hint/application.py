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
    LOGGER.info("device listener start")

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
    LOGGER.info("device listener stop")

    server.shutdown()


def attach(message_content):
    """
    Sends HINT an attach message.

    :param message_content:
    :return:
    """
    LOGGER.info("sending attach to HINT")

    hint_req_mod.attach(message_content)
