import logging
import requests

from hint_controller.util.args import get_arg, HINT_IP_ADDRESS, HINT_PORT, \
    HUME_UUID

import hume_storage as storage

from hint_controller.hint.models import HumeUser, BrokerCredentials


LOGGER = logging.getLogger(__name__)


"""
This module provides functions for sending requests to HINT.
"""


SESSION_ID = None


def _hint_api_url():
    """Returns the HINT API URL."""
    return "http://" + \
           get_arg(HINT_IP_ADDRESS) + \
           ':' + str(get_arg(HINT_PORT)) + \
           "/api/"


def pair():
    """
    Pairing procedure. Login will follow a successful pairing.
    """
    LOGGER.info("sending pairing request")

    response = requests.post(_hint_api_url() + "humes/",
                             json={"uuid": get_arg(HUME_UUID)})

    if response.status_code == 201:
        response_content = response.json()  # Contains login information.
        LOGGER.debug(f"successful pairing, new hume user: {response_content}")

        user_info = response_content['hume_user']
        username = user_info['username']
        password = user_info['password']

        hume_user = HumeUser(username=username, password=password)
        storage.save(hume_user)

        if login(hume_user):
            broker_credentials()
        else:
            LOGGER.error("failed to get broker credentials")
    else:
        # Either format error (caused by what?) or UUID taken. Either case,
        # severe error
        LOGGER.error("paring failed")


def login(hume_user):
    """
    Login procedure to authenticate with HINT.

    :return: True if successful
    """
    LOGGER.info("logging in to HINT")

    response = requests.post(_hint_api_url() + "users/login",
                             json={"username": hume_user.username,
                                   "password": hume_user.password})

    if response.status_code == 200:
        global SESSION_ID
        SESSION_ID = response.cookies.get("sessionid")
        LOGGER.debug(f"session id set to: {SESSION_ID}")

        return True
    else:
        LOGGER.error("failed to log in to HINT")


def broker_credentials():
    """
    Requests broker credentials from HINT.
    """
    LOGGER.info("requesting broker credentials")

    response = requests.get(_hint_api_url() + "humes/broker-credentials",
                            cookies={"sessionid": SESSION_ID})

    broker_credentials = response.json()
    storage.save(BrokerCredentials(username=broker_credentials['username'],
                                   password=broker_credentials['password']))


def attach(message_content):
    """
    Sends HINT an attach message.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"sending HINT attach message: {message_content}")


def device_event(message_content):
    """
    Sends HINT an event message.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"sending HINT device event message: {message_content}")


def sub_device_event(message_content):
    """
    Sends HINT an event message.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"sending HINT event message: {message_content}")
