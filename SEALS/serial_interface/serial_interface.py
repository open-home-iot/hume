from select import select
from serial import Serial
from threading import Thread

from serial_interface import event_handler


# Serial connection
CONNECTION = None


def decode(message):
    """

    :param message:
    :return:
    """
    decoded_string = message.decode('utf-8')
    return decoded_string.strip()


def encode(message):
    """

    :param message:
    :return:
    """
    return message.encode('utf-8')


def send_message(message):
    """

    :param message:
    :return:
    """
    message = encode(message)
    CONNECTION.write(message)


def reply(main, sub):
    """

    :param main:
    :param sub:
    :return:
    """
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
    """

    :return:
    """
    event_handler.writer_thread.start()
    listener_daemon = Thread(target=serial_select, kwargs={'serial_port': serial_port, 'baudrate': baudrate}, daemon=True)
    listener_daemon.start()
