_args = None

HUME_UUID = "hume_uuid"
DEVICE_MOCK_ADDRESS = "device_mock_address"


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
    return _args.get(name)
