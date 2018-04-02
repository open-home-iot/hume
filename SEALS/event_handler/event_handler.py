import requests

from threading import Thread, Event

from queue import Queue

try:
    from camera.snapshot import concurrent_snapshot
except ImportError:
    def concurrent_snapshot():
        print('PICAMERA NOT AVAILABLE')

from event_handler.events import *
from serial_interface import serial_interface


writer_thread = None


class EventThread(Thread):

    def __init__(self, *args, **kwargs):
        super(EventThread, self).__init__(*args, **kwargs)
        self.event = Event()
        self.alarm_raised = False
        self.awaiting_reply = False
        self.reply_message = None
        self.command_buffer = Queue()

    def run(self):
        print("Command waiter started")
        while True:
            self.event.wait()
            self.awaiting_reply = True  # Semaphore set to prevent another event interrupting.
            self.event.clear()  # If the flag is not cleared, the next wait will return immediately.

            handler, command = self.command_buffer.get()
            print("SERI SERVER: Got command: ", command)
            if command == 'shutdown':
                break

            serial_interface.send_message(str(command))  # Send a message to the Arduino

            # Wait for reply.
            try:
                print("SERI SERVER: Waiting for reply from arduino")
                self.event.wait(timeout=2.0)
            except TimeoutError:
                print("SERI SERVER: Reply timed out")
                self.reply_message = EVENT[ERR]
            finally:
                self.event.clear()  # Keep a cleared event flag!
                notify_reply(handler)
                self.awaiting_reply = False


def alarm_raised(sub):
    writer_thread.alarm_raised = sub == EVENT_SUB_CAUSE[ON]
    print("SERI SERVER: Alarm is raised: ", writer_thread.alarm_raised)
    serial_interface.reply(PROXIMITY_ALARM, sub)

    alarm_status = 'on' if sub == '1' else 'off'
    if alarm_status == 'on':
        concurrent_snapshot()

    requests.get('http://localhost:8000/api/events/alarm/' + alarm_status)


def reply_received(sub):
    writer_thread.reply_message = sub
    writer_thread.event.set()


def get_distance(sub):
    reply_received(sub)


def error(sub):
    print("An error was received!")


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
    if writer_thread.awaiting_reply:
        handler.resolve_wait()
        return

    writer_thread.command_buffer.put((handler, command))
    writer_thread.event.set()


def notify_reply(handler):
    print("SERI SERVER: Notifying HTTP SERVER")
    handler.resolve_wait(reply=writer_thread.reply_message)


def start():
    global writer_thread
    writer_thread = EventThread()
    writer_thread.start()
