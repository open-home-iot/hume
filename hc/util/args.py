"""
This module is responsible for keeping CLI arguments stored for easy access.
"""


_args: dict

HUME_UUID = "hume_uuid"

HINT_IP_ADDRESS = "hint_ip_address"
HINT_PORT = "hint_port"
BROKER_IP_ADDRESS = "broker_ip_address"
BROKER_PORT = "broker_port"


def set_args(**cli_args):
    """
    Assigns input kwargs to internal _args.
    """
    global _args
    _args = cli_args


def get_arg(name):
    """
    Get argument with name.

    :param name: argument to get
    """
    return _args.get(name)  # noqa
