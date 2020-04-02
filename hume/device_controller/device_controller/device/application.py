import threading
import logging


from bottle import run
from . import routes  # To load routes


LOGGER = logging.getLogger(__name__)


def start():
    """
    Starts up the HTTP listener.
    """
    def start_http_server():
        """
        Starts an HTTP server locally on port 8081.
        """
        run(host='localhost', port=8081)

    LOGGER.info("device listener start")

    # TODO well, what will be used to communicate with devices?
    thread = threading.Thread(target=start_http_server)
    thread.start()


def stop():
    """
    Stop the HTTP listener.
    """
    LOGGER.info("device listener stop")
