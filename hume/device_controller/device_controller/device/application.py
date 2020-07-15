import threading
import logging

from bottle import run

import hume_storage as storage

from .http_server import MyServer
from .models import *
from . import routes  # To load routes
from .settings import req_mod


LOGGER = logging.getLogger(__name__)

server = MyServer(host='localhost', port=8081)
server_thread: threading.Thread


def start():
    """
    Starts up the HTTP listener.
    """
    LOGGER.info("device listener start")

    storage.register(Device)

    def start_http_server():
        """
        Starts an HTTP server locally on port 8081. This is the server that
        devices will send requests to.
        """
        run(server=server)  # Blocks!
        LOGGER.info("device listener broke server loop")

    global server_thread
    server_thread = threading.Thread(target=start_http_server)
    server_thread.start()


def stop():
    """
    Stop the HTTP listener.
    """
    LOGGER.info("device listener stop")

    server.shutdown()
    server_thread.join()


def device_action(device, action_id):
    """
    Sends a device an action invocation.

    :param device:
    :param action_id:
    """
    LOGGER.info("sending device action to device")

    req_mod().device_action(device, action_id)


def sub_device_action(device, device_id, action_id):
    """
    Sends a sub device an action invocation.

    :param device:
    :param device_id:
    :param action_id:
    """
    LOGGER.info("sending sub device action to device")

    req_mod().sub_device_action(device, device_id, action_id)
