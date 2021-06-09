"""
This module is responsible for keeping CLI arguments stored for easy access.
"""


_args: dict

HUME_UUID = "hume_uuid"

# TESTING PARAMETERS
TEST_DEVICE_MOCK_ADDRESS = "test_device_mock_address"
TEST_RUN_DEVICE_SIMULATOR = "test_run_device_simulator"


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
