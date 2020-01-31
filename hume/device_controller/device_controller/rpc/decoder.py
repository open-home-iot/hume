import json


def decode(message: bytes):
    """
    Decodes an RPC request's message body.

    :param bytes message: encoded message
    :return dict decoded_message: decoded message
    """
    return json.loads(message.decode('utf-8'))
