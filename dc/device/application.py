import threading
import logging

from bottle import run

import hume_storage as storage

from device.http_server import MyServer
from device.models import Device
from device import routes  # noqa
from util.args import get_arg, TEST_RUN_DEVICE_SIMULATOR


LOGGER = logging.getLogger(__name__)

server = MyServer(host='localhost', port=8081)
server_thread: threading.Thread


def model_init():
    """
    Initialize models.
    """
    LOGGER.info("model-init")
    storage.register(Device)


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")


def start():
    """
    Starts up the HTTP listener.
    """
    LOGGER.info("device listener start")

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

    if get_arg(TEST_RUN_DEVICE_SIMULATOR):
        from dc.device.simulator import start_simulator
        start_simulator()


def stop():
    """
    Stop the HTTP listener.
    """
    LOGGER.info("device listener stop")

    server.shutdown()
    server_thread.join()

    if get_arg(TEST_RUN_DEVICE_SIMULATOR):
        from dc.device.simulator import stop_simulator
        stop_simulator()
