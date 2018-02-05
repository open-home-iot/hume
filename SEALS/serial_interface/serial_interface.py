from queue import Queue
from select import select
from serial import Serial
from threading import Thread, Event

from SEALS.serial_interface.events import *
from SEALS import http_server


# State objects
ALARM_RAISED = False


# Messaging mechanisms
AWAITING_REPLY = False
REPLY_MESSAGE = None

COMMAND_BUFFER = Queue()


# Serial connection
CONNECTION = Serial(port='/dev/tty.usbmodem1411', baudrate=9600)


class EventThread(Thread):
    """

    """

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super(EventThread, self).__init__(*args, **kwargs)
        self.event = Event()

    def run(self):
        """

        :return:
        """
        global AWAITING_REPLY
        global REPLY_MESSAGE
        print("Command waiter started")
        while True:
            self.event.wait()

            # Prevents a new command from interrupting the current sequence.
            AWAITING_REPLY = True

            handler, command = COMMAND_BUFFER.get()
            print("SERI SERVER: Got command: ", command)
            send_message(str(command))

            # Wait for reply.
            try:
                print("SERI SERVER: Waiting for reply from arduino")
                self.event.wait(timeout=2.0)
            except TimeoutError:
                print("SERI SERVER: Reply timed out")
                REPLY_MESSAGE = str(ERR)
            finally:
                notify_reply(handler)
                AWAITING_REPLY = False


writer_thread = EventThread()


def start():
    """

    :return:
    """
    writer_thread.start()
    listener_daemon = Thread(target=serial_select, daemon=True)
    listener_daemon.start()


def serial_select():
    """

    :return:
    """
    print("Select waiter started")
    while True:
        # Since no timeout is specified, block until read is available
        # ------------------------------
        # BLOCKS
        select([CONNECTION], [], [])
        # ------------------------------
        
        event = CONNECTION.readline()
        event_notification(decode(event))


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


def alarm_raised(sub):
    """

    :param sub:
    :return:
    """
    global ALARM_RAISED
    ALARM_RAISED = sub == ON
    print("SERI SERVER: Alarm is raised: ", ALARM_RAISED)
    reply(PROXIMITY_ALARM, sub)


def reply_received(sub):
    """

    :param sub:
    :return:
    """
    global REPLY_MESSAGE
    REPLY_MESSAGE = sub
    writer_thread.event.set()


def get_distance(sub):
    """

    :param sub:
    :return:
    """
    print("SERI SERVER: Got distance reply")
    reply_received(sub)


def error(sub):
    """

    :param sub:
    :return:
    """
    print("An error was received!")


def event_notification(event):
    """

    :param event:
    :return:
    """
    event_info = event.split(" ")

    if len(event_info) > 1:
        main, sub = event_info
        events[main](sub)
    else:
        events[event_info[0]]()


events = {
        "0": alarm_raised,
        "5": get_distance,
        "9": error,
    }


def execute_command(handler, command):
    """

    :param command:
    :param handler:
    :return:
    """
    # TODO: Add handling for busy, return cause code etc.
    if AWAITING_REPLY:
        return

    COMMAND_BUFFER.put((handler, command))
    writer_thread.event.set()


def notify_reply(handler):
    """

    :param handler:
    :return:
    """
    handler.resolve_wait(REPLY_MESSAGE)
