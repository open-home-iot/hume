import argparse

from http_server import http_server
from serial_interface import serial_interface
from event_handler import event_handler


DEFAULT_BAUDRATE = 9600   # Baudrate of the serial interface
DEFAULT_IP = '127.0.0.1'  # IP of this HTTP event server
DEFAULT_PORT = 8080       # Port of this HTTP event server


def parse_arguments():
    parser = argparse.ArgumentParser(description='SEALS, Serial Event And hTTP Listening Service.')
    parser.add_argument('--serial_port', type=str, required=True)
    parser.add_argument('--baudrate', type=int)
    parser.add_argument('--ip', type=str)
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    print(args)
    return args


if __name__ == '__main__':
    args = parse_arguments()

    # Required arguments
    serial_port = args.serial_port

    # Optional arguments
    baudrate = args.baudrate if args.baudrate is not None else DEFAULT_BAUDRATE
    target_ip = args.ip if args.ip is not None else DEFAULT_IP
    target_port = args.port if args.port is not None else DEFAULT_PORT

    serial_interface.start(serial_port, baudrate)
    event_handler.start()
    http_server.start((target_ip, target_port))
