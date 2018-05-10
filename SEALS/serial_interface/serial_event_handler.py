import requests

from requests import exceptions as request_exceptions

from queue import Queue

try:
    from camera.snapshot import concurrent_snapshot
except ImportError:
    def concurrent_snapshot():
        print('SERI SERVER: PICAMERA NOT AVAILABLE')

from events.events import *
from events.event_handler import EventThread
from serial_interface import serial_interface


writer_thread = None
alarm_status = False


class SerialEventHandler(EventThread):

    def __init__(self, *args, **kwargs):
        super(SerialEventHandler, self).__init__(*args, **kwargs)

        self.awaiting_reply = False
        self.reply = None
        self.command_buffer = Queue()

    def run(self):
        print("SERI SERVER: Event handler started")

        while 1:
            self.wait()  # Wait for notify

            self.awaiting_reply = True  # Semaphore set to prevent another event interrupting.
            self.clear()  # If the flag is not cleared, the next wait will return immediately.

            handler, command = self.command_buffer.get()
            print("SERI SERVER: Got command: ", command)
            if command == 'shutdown':
                break

            serial_interface.send_message(str(command))  # Send a message to the Arduino

            # Wait for reply.
            print("SERI SERVER: Waiting for reply from arduino")
            self.wait(timeout=2.0)

            self.clear()  # Keep a cleared event flag!
            handler.notify_reply(reply=self.reply)
            self.awaiting_reply = False

    def busy(self):
        return self.awaiting_reply

    def execute_command(self, command):
        self.command_buffer.put(command)
        self.event.set()

    def send_reply(self, reply):
        self.reply = reply
        self.event.set()


def alarm_raised(sub):
    global alarm_status
    alarm_status = sub == EVENT_SUB_CAUSE[ON]
    print("SERI SERVER: Alarm status is: ", alarm_status)
    serial_interface.reply(PROXIMITY_ALARM, sub)  # Ack towards arduino

    # Snap a picture if alarm was turned on
    if alarm_status:
        concurrent_snapshot()

    # Notify frontend
    alarm_url = 'on' if alarm_status else 'off'
    try:
        requests.get('http://localhost:8000/api/events/alarm/' + alarm_url)
    except request_exceptions.ConnectionError:
        print('SERI SERVER: Could not notify HTTP server of event, unreachable')


def error(sub):
    print("SERI SERVER: An error was received!")


def reply_received(sub):
    writer_thread.send_reply(sub)


def get_distance(sub):
    reply_received(sub)


def event_notification(event):
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
    if writer_thread.busy():
        handler.notify_reply()
        return

    writer_thread.execute_command((handler, command))


def start():
    global writer_thread
    writer_thread = SerialEventHandler()
    writer_thread.start()
