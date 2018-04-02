import argparse

from http_server import http_server
from serial_interface import serial_interface
from event_handler import event_handler


DEFAULT_SERIAL_PORT = '/dev/ttyACM0'
DEFAULT_BAUDRATE = 9600
DEFAULT_IP = ''
DEFAULT_PORT = 8080


def parse_arguments():
    parser = argparse.ArgumentParser(description='SEALS, Serial Event And hTTP Listening Service.')
    parser.add_argument('--serial_port', type=str)
    parser.add_argument('--baudrate', type=int)
    parser.add_argument('--ip', type=str)
    parser.add_argument('--port', type=int)
    parser.add_argument('--standalone', type=bool)  # NI
    args = parser.parse_args()
    print(args)
    return args


if __name__ == '__main__':
    args = parse_arguments()

    serial_port = args.serial_port if args.serial_port is not None else DEFAULT_SERIAL_PORT
    baudrate = args.baudrate if args.baudrate is not None else DEFAULT_BAUDRATE
    ip = args.ip if args.ip is not None else DEFAULT_IP
    port = args.port if args.port is not None else DEFAULT_PORT

    serial_interface.start(serial_port=serial_port, baudrate=baudrate)
    event_handler.start()
    http_server.start(server_address=(ip, port))
