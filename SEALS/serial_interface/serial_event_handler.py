from http_server import web_interface

from queue import Queue

try:
    from camera.snapshot import concurrent_snapshot
except ImportError:
    def concurrent_snapshot():
        print('SERI SERVER: PICAMERA NOT AVAILABLE')

from events.events import *
from serial_interface import serial_interface


alarm_status = False


def execute_command(handler, command):
    event_handler.execute_command((handler, command))


class SerialEventHandler:

    def __init__(self, *args, **kwargs):
        super(SerialEventHandler, self).__init__(*args, **kwargs)

        self.handler = None

    def execute_command(self, command):
        handler, c = command
        if self.handler:
            handler.notify()
            return
        else:
            self.handler = handler  # Semaphore set to prevent another event interrupting.

        serial_interface.send_message(str(command))

    def reply(self, reply):
        self.handler.notify(reply=reply)
        self.handler = None


event_handler = SerialEventHandler()


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
    web_interface.notify_alarm(alarm_url)


def error(sub):
    print("SERI SERVER: An error was received!")


def reply_received(sub):
    event_handler.reply(sub)


def get_alarm_status(sub):
    reply_received(sub)


def set_alarm_state(sub):
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
        EVENT[GET_ALARM_STATUS]: get_alarm_status,
        EVENT[SET_ALARM_STATE]: set_alarm_state,
        EVENT[ERR]: error,
    }
