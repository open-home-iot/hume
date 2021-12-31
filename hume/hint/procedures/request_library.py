import logging
import requests

from util import get_arg
from defs import CLI_HINT_IP_ADDRESS, CLI_HINT_PORT, CLI_HUME_UUID
from hint.models import HumeUser


LOGGER = logging.getLogger(__name__)


"""
This module provides functions for sending HTTP requests to HINT.
"""


def _hint_api_url():
    """Returns the HINT API URL."""
    return "http://" + \
           get_arg(CLI_HINT_IP_ADDRESS) + \
           ':' + str(get_arg(CLI_HINT_PORT)) + \
           "/api/"


def pair():
    """
    Send a pairing request.

    :returns: result of the pairing request, None if failed
    :rtype: dict | None
    """
    LOGGER.info("sending pairing request")

    response = requests.post(_hint_api_url() + "humes",
                             json={"uuid": get_arg(CLI_HUME_UUID)})

    if response.status_code == requests.codes.created:
        response_content = response.json()  # Contains login information.
        LOGGER.debug(f"successful pairing, response: {response_content}")

        user_info = response_content['hume_user']

        return user_info

    # Either format error (caused by what?) or UUID taken. Either case,
    # severe error
    LOGGER.error("paring request failed")


def login(hume_user: HumeUser):
    """
    Login procedure to authenticate with HINT.

    :param hume_user: HUME user account information
    :returns: result of the login request
    :rtype: tuple
    """
    LOGGER.info("logging in to HINT")

    response = requests.post(_hint_api_url() + "users/login",
                             json={"username": hume_user.username,
                                   "password": hume_user.password})

    print(response.cookies)

    if response.status_code == requests.codes.ok:
        session_id = response.cookies.get("sessionid")
        csrf_token = response.cookies.get("csrftoken")
        LOGGER.debug(f"session id gotten: {session_id}")

        return session_id, csrf_token

    LOGGER.error("failed to log in to HINT")


def broker_credentials(session_id):
    """
    Requests broker credentials from HINT.

    :param session_id: session ID to authenticate the request
    :returns: broker credentials
    :rtype: dict | None
    """
    LOGGER.info("requesting broker credentials")

    response = requests.get(_hint_api_url() + "humes/broker-credentials",
                            cookies={"sessionid": session_id})

    print(response.cookies)

    if response.status_code == requests.codes.ok:
        return response.json()


def create_device(capabilities: dict,
                  session_id: str,
                  csrf_token: str) -> bool:
    """
    Sends a create device request to HINT with the provided capabilities.

    :param capabilities: HOME-compliant capabilities, to be encoded as JSON
    :param session_id: session ID to authenticate the request
    :param csrf_token: CSRF token
    :return: True if successful
    """
    LOGGER.info("sending create device request")

    response = requests.post(
        f"{_hint_api_url()}humes/{get_arg(CLI_HUME_UUID)}/devices",
        json=capabilities,
        cookies={"sessionid": session_id,
                 "csrftoken": csrf_token},
        headers={"X-CSRFToken": csrf_token})

    print(response.cookies)

    if response.status_code == requests.codes.created:
        return True
    return False
