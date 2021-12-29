from device.connection.ble.defs import MSG_START


def has_message_start(data: bytearray):
    """Checks if the input data is the start of a device message."""
    return data[0] == ord(MSG_START)


def get_request_type(data: bytearray) -> int:
    """:returns: the message request type"""
    return int(chr(data[1]))
