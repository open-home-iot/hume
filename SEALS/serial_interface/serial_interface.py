from select import select
from serial import Serial
from threading import Thread

from event_handler import event_handler

# Serial connection
CONNECTION = None


def decode(message):
    decoded_string = message.decode('utf-8')
    return decoded_string.strip()


def encode(message):
    return message.encode('utf-8')


def send_message(message):
    message = encode(message)
    CONNECTION.write(message)


def reply(main, sub):
    send_message(str(main) + ' ' + str(sub))


def serial_select(serial_port='', baudrate=9600):
    """

    :return:
    """
    global CONNECTION

    CONNECTION = Serial(port=serial_port, baudrate=baudrate)
    print("Select waiter started")
    while True:
        # Since no timeout is specified, block until read is available
        # ------------------------------
        # BLOCKS
        select([CONNECTION], [], [])
        # ------------------------------

        event = CONNECTION.readline()
        event_handler.event_notification(decode(event))


def start(serial_port='', baudrate=9600):
    listener = Thread(target=serial_select,
                      kwargs={'serial_port': serial_port, 'baudrate': baudrate})
    listener.start()
