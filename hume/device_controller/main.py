import argparse

from device_controller.configuration.server import ConfigServer
from device_controller.root import RootApp
from device_controller.rpc.server import RPCServer
from device_controller.utility.dispatch import dispatcher
from device_controller.zigbee.server import ZigbeeServer


def parse_args():
    """
    Parse arguments provided at running the python program.
    """
    parser = argparse.ArgumentParser(description="HUME device_controller controller")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    root_app = RootApp(cli_args=args)
    root_app.start()

    # To block on start to test
    inp = input()

    dispatcher.dispatch(ZigbeeServer.dispatch_id,
                        "message for the zigbee server")
    dispatcher.dispatch(ConfigServer.dispatch_id,
                        "message for the config server")
    dispatcher.dispatch(RPCServer.dispatch_id,
                        "message for the config server")
