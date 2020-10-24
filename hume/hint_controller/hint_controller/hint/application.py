import threading
import logging

from bottle import run

import hume_storage as storage

from hint_controller.hint.http_server import MyServer
from hint_controller.hint.models import Hume
from hint_controller.hint.settings import req_mod
from hint_controller.hint import routes  # noqa, imported to load routes
from hint_controller.hint.util import read_hume_id


LOGGER = logging.getLogger(__name__)

server = MyServer(host='localhost', port=8082)
server_thread: threading.Thread


def start():
    """
    Starts up the HTTP listener.
    """
    LOGGER.info("hint start")

    storage.register(Hume)

    def start_http_server():
        """
        Starts an HTTP server locally on port 8082. This sever listens for
        requests sent from the cloud (HINT).
        """
        run(server=server)  # Blocks!

    global server_thread
    server_thread = threading.Thread(target=start_http_server)
    server_thread.start()

    hume_id = read_hume_id()
    hume = storage.get(Hume, hume_id)

    if hume is None:
        hume = Hume(hume_id=hume_id)

        storage.save(hume)
    elif hume.paired:
        LOGGER.debug("HUME is already paired")
        return
    else:
        pass

    req_mod().pair(hume)


def stop():
    """
    Stop the HTTP listener.
    """
    LOGGER.info("hint stop")

    server.shutdown()
    server_thread.join()


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
