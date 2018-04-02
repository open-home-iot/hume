import requests

from threading import Thread, Event

from queue import Queue

from camera.snapshot import concurrent_snapshot

from serial_interface.events import *
from serial_interface import serial_interface


# State objects
ALARM_RAISED = False
AWAITING_REPLY = False

# Messaging mechanisms
REPLY_MESSAGE = None

COMMAND_BUFFER = Queue()


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
            self.event.clear()  # If the flag is not cleared, the next wait will return immediately.

            # Prevents a new command from interrupting the current sequence.
            AWAITING_REPLY = True

            handler, command = COMMAND_BUFFER.get()
            print("SERI SERVER: Got command: ", command)
            if command == 'shutdown':
                break

            serial_interface.send_message(str(command))

            # Wait for reply.
            try:
                print("SERI SERVER: Waiting for reply from arduino")
                self.event.wait(timeout=2.0)
            except TimeoutError:
                print("SERI SERVER: Reply timed out")
                REPLY_MESSAGE = EVENT[ERR]
            finally:
                self.event.clear()  # Keep a cleared event flag!
                notify_reply(handler)
                AWAITING_REPLY = False


writer_thread = EventThread()


def alarm_raised(sub):
    """

    :param sub:
    :return:
    """
    global ALARM_RAISED
    ALARM_RAISED = sub == EVENT_SUB_CAUSE[ON]
    print("SERI SERVER: Alarm is raised: ", ALARM_RAISED)
    serial_interface.reply(PROXIMITY_ALARM, sub)

    alarm_status = 'on' if sub == '1' else 'off'
    if alarm_status == 'on':
        concurrent_snapshot()
        print("hi")

    requests.get('http://localhost:8000/api/events/alarm/' + alarm_status)


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
    print("SERI SERVER: Event notification: ", event)
    event_info = event.split(" ")

    if len(event_info) > 1:
        main, sub = event_info
        events[main](sub)
    else:
        events[event_info[0]]()


events = {
        EVENT[PROXIMITY_ALARM]: alarm_raised,
        EVENT[GET_DISTANCE]: get_distance,
        EVENT[ERR]: error,
    }


def execute_command(handler, command):
    """

    :param command:
    :param handler:
    :return:
    """
    global AWAITING_REPLY
    if AWAITING_REPLY:
        handler.resolve_wait()
        return

    COMMAND_BUFFER.put((handler, command))
    writer_thread.event.set()


def notify_reply(handler):
    """

    :param handler:
    :return:
    """
    print("SERI SERVER: Notifying HTTP SERVER")
    handler.resolve_wait(reply=REPLY_MESSAGE)
