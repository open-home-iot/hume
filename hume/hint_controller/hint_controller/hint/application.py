import threading
import logging

from bottle import run

import hume_storage as storage

from hint_controller.hint.http_server import MyServer
from hint_controller.hint.models import HumeUser, BrokerCredentials
from hint_controller.hint import routes  # noqa, imported to load routes
from hint_controller.hint import hint_req_lib


LOGGER = logging.getLogger(__name__)

server = MyServer(host='localhost', port=8082)
server_thread: threading.Thread


def start():
    """
    Starts up the HTTP listener.
    """
    LOGGER.info("hint start")

    def model_init():
        """
        Initialize models.
        """
        storage.register(HumeUser)
        storage.register(BrokerCredentials)

    def start_http_server():
        """
        Starts an HTTP server locally on port 8082. This server listens for
        requests sent from the cloud (HINT).
        """
        def run_server():
            """Start the bottle server"""
            run(server=server)  # Blocks!

        global server_thread
        server_thread = threading.Thread(target=run_server)
        server_thread.start()

    def startup_actions():
        """
        Run through the HINT application's startup actions.
        """
        hume_user = storage.get(HumeUser, None)

        if hume_user is None:
            # Send pairing request
            hint_req_lib.pair()
        else:
            # Or login if user already exists
            if hint_req_lib.login(hume_user):
                hint_req_lib.broker_credentials()

    model_init()
    start_http_server()
    startup_actions()


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

    pass


def device_event(message_content):
    """
    Sends HINT a device event message

    :param message_content:
    :return:
    """
    LOGGER.info("sending device event to HINT")

    pass


def sub_device_event(message_content):
    """
    Sends HINT a sub device event message

    :param message_content:
    :return:
    """
    LOGGER.info("sending sub device event to HINT")

    pass
