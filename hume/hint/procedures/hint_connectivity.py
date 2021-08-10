import logging
import sys

import storage as storage

from hint.procedures import request_library
from hint.models import HumeUser, BrokerCredentials, HintAuthentication


LOGGER = logging.getLogger(__name__)


def pair():
    """HUME pairing procedure. Will exit on failure."""
    LOGGER.info("starting HUME pairing procedure...")

    """
    Register the HUME
    """
    user_info = request_library.pair()
    if user_info is not None:
        LOGGER.info("HINT pairing successful, got generated HUME credentials")
        username = user_info['username']
        password = user_info['password']
        hume_user = HumeUser(username=username, password=password)
        storage.save(hume_user)
    else:
        LOGGER.critical("failed to register HUME with HINT")
        sys.exit(1)

    """
    Authenticate with gotten credentials
    """
    if not login_to_hint(hume_user):
        LOGGER.critical("failed to authenticate with HINT")
        sys.exit(1)
    LOGGER.info("logged in to HINT")

    """
    Fetch broker credentials
    """
    LOGGER.info("setting up broker credentials")

    # Fetch newly stored HINT credentials
    hint_auth = storage.get(HintAuthentication, None)
    broker_credentials = request_library.broker_credentials(
        hint_auth.session_id
    )
    if broker_credentials:
        LOGGER.info("got broker credentials")
        username = broker_credentials['username']
        password = broker_credentials['password']
        new_broker_credentials = BrokerCredentials(
            username=username,
            password=password,
        )
        storage.save(new_broker_credentials)
    else:
        LOGGER.critical("broker credentials fetch failed")
        sys.exit(1)


def unpair():
    pass


def login_to_hint(hume_user):
    """
    Log in to HINT and store the authentication token for future use.

    :param hume_user: HumeUser
    :returns: True on success, else False
    """
    result = request_library.login(hume_user)
    if result is not None:
        LOGGER.info("logged in to HINT")
        session_id, csrf_token = result
        hint_auth = HintAuthentication(session_id, csrf_token=csrf_token)
        storage.save(hint_auth)
        return True

    LOGGER.error("failed to authenticate with HINT")
    return False

