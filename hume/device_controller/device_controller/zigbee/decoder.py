import json


def decode(message: bytes):
    return json.loads(message.decode('utf-8'))
