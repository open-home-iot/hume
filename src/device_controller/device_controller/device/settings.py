from . import device_req_lib


# Override this module to insert mocking mods/simulators. It will make sure
# outbound device traffic gets sent via the set module's implementation of the
# device interface.
_device_req_mod = device_req_lib


def req_mod():
    """
    Returns the request module used to send messages to devices.
    :return:
    """
    return _device_req_mod
