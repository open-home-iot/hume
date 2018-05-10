import argparse

from http_server import http_server
from serial_interface import serial_interface
from event_handler import event_handler


DEFAULT_SERIAL_PORT = '/dev/ttyACM0'
DEFAULT_BAUDRATE = 9600
DEFAULT_IP = '192.168.0.10'
DEFAULT_PORT = 8080


def parse_arguments():
    parser = argparse.ArgumentParser(description='SEALS, Serial Event And hTTP Listening Service.')
    parser.add_argument('--serial_port', type=str)
    parser.add_argument('--baudrate', type=int)
    parser.add_argument('--target_ip', type=str)
    parser.add_argument('--target_port', type=int)
    args = parser.parse_args()
    print(args)
    return args


if __name__ == '__main__':
    args = parse_arguments()

    serial_port = args.serial_port if args.serial_port is not None else DEFAULT_SERIAL_PORT
    baudrate = args.baudrate if args.baudrate is not None else DEFAULT_BAUDRATE
    target_ip = args.ip if args.ip is not None else DEFAULT_IP
    target_port = args.port if args.port is not None else DEFAULT_PORT

    serial_interface.start(serial_port=serial_port, baudrate=baudrate)
    event_handler.start()
    http_server.start(server_address=(target_ip, target_port))
