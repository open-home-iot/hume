import logging
import sys
import os
# To be able to import from the lib package
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from lib import RMQClient


def callback(message: bytes):
    print("Got message: {}".format(message))


if __name__ == "__main__":
    print("Starting")

    client = RMQClient(log_level=logging.INFO)
    client.start()
    client.subscribe("test1", callback)

    while True:
        inp = input()

        if inp == "1":
            client.publish("test1", b'messaging the test1 topic')
