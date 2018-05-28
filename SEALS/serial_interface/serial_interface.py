from select import select
from serial import Serial
from threading import Thread

from serial_interface import serial_event_handler


serial_port = None


"""
The serial interface does not have a corresponding shutdown handler since it is run as a daemon
"""


def decode(message):
    decoded_string = message.decode('utf-8')
    return decoded_string.strip()


def encode(message):
    return message.encode('utf-8')


def send_message(main, sub):
    message = main + ' ' + sub
    message = encode(message)
    print('SERI INTERFACE: Sending message: ', message)
    serial_port.write(message)


def read_incoming_data():
    event = decode(serial_port.readline())
    serial_event_handler.event_notification(event)

    read_loop()


def read_loop():
    select([serial_port], [], [])
    read_incoming_data()


def init_serial_port(port, baudrate):
    global serial_port
    serial_port = Serial(port=port, baudrate=baudrate)
    print("SERI SERVER: Selecting on port: ", port)
    read_loop()


def start(port, baudrate):
    listener = Thread(target=init_serial_port,
                      args=(port, baudrate),
                      daemon=True)
    # The significance of this flag is that the entire Python program exits when only daemon threads are left. The
    # serial interface will then shutdown once HTTP server and the event handler are both shut down.
    listener.start()
