import threading
import logging

from bottle import run

import hume_storage as storage

from .http_server import MyServer
from .models import *
from . import routes  # To load routes
from .settings import device_req_mod


LOGGER = logging.getLogger(__name__)

server = MyServer(host='localhost', port=8081)


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

    thread = threading.Thread(target=start_http_server)
    thread.start()


def stop():
    """
    Stop the HTTP listener.
    """
    LOGGER.info("device listener stop")

    server.shutdown()


def confirm_attach(device):
    """
    Sends a device confirm attach.

    :param device:
    """
    LOGGER.info("sending confirm attach to device")

    device_req_mod.confirm_attach(device)


def device_action(device, action_id):
    """
    Sends a device an action invocation.

    :param device:
    :param action_id:
    """
    LOGGER.info("sending device action to device")

    device_req_mod.device_action(device, action_id)


def sub_device_action(device, device_id, action_id):
    """
    Sends a sub device an action invocation.

    :param device:
    :param device_id:
    :param action_id:
    """
    LOGGER.info("sending sub device action to device")

    device_req_mod.sub_device_action(device, device_id, action_id)
