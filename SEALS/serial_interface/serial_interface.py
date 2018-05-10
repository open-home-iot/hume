from select import select
from serial import Serial
from threading import Thread

from event_handler import event_handler


serial_port = None


def decode(message):
    decoded_string = message.decode('utf-8')
    return decoded_string.strip()


def encode(message):
    return message.encode('utf-8')


def send_message(message):
    message = encode(message)
    serial_port.write(message)


def reply(main, sub):
    send_message(str(main) + ' ' + str(sub))


def read_incoming_data():
    event = decode(serial_port.readline())
    event_handler.event_notification(event)

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
                      args=(port, baudrate))
    listener.start()
