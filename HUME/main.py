import argparse
import signal
import requests

from threading import Thread
from http_server import http_server
from serial_interface import serial_interface


DEFAULT_BAUDRATE = 9600  # Baudrate of the serial interface
DEFAULT_IP = ''          # IP of this HTTP event server
DEFAULT_PORT = 8080      # Port of this HTTP event server

ip = ''
port = ''


def parse_arguments():
    parser = argparse.ArgumentParser(description='HUME, HOME Hub.')
    parser.add_argument('--serial_port', type=str, required=True)
    parser.add_argument('--baudrate', type=int)
    parser.add_argument('--ip', type=str)
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    print(args)
    return args


def send_shutdown(target_address):
    requests.get('http://' + target_address + ':' + str(port) + '/shutdown')


def handle_sigint(signal, frame):
    target_address = 'localhost' if ip == '' else ip
    shutdown_thread = Thread(target=send_shutdown, args=(target_address,), daemon=True)
    shutdown_thread.start()


if __name__ == '__main__':
    args = parse_arguments()

    # Required arguments
    serial_port = args.serial_port

    # Optional arguments
    baudrate = args.baudrate if args.baudrate is not None else DEFAULT_BAUDRATE
    ip = args.ip if args.ip is not None else DEFAULT_IP
    port = args.port if args.port is not None else DEFAULT_PORT

    # Needs to be declared after argument parsing but before starting services
    signal.signal(signal.SIGINT, handle_sigint)

    # Start necessary services
    serial_interface.start(serial_port, baudrate)
    http_server.start((ip, port))
