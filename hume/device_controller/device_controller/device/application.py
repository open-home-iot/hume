import threading
import logging

from bottle import run

from device_controller.util import storage

from .http_server import MyServer
from .models import *
from . import routes  # To load routes
from . import device_req_lib
from .settings import device_req_mod


LOGGER = logging.getLogger(__name__)

server = MyServer(host='localhost', port=8081)


def start():
    """
    Starts up the HTTP listener.
    """
    storage.register(Device)

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


def confirm_attach(device):
    """
    Sends a device a message.

    :param device:
    :return:
    """
    # Send a confirmation to the device
    device_req_mod.confirm_attach(device)


def device_action(device, action_id):
    """
    Sends a device an action invocation.

    :param device:
    :param action_id:
    :return:
    """
    device_req_mod.device_action(device, action_id)


def sub_device_action(device, device_id, action_id):
    """
    Sends a sub device an action invocation.

    :param device:
    :param device_id:
    :param action_id:
    :return:
    """
    device_req_mod.sub_device_action(device, device_id, action_id)
