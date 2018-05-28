from http_server import http_requests

from datetime import datetime

from configuration.active_config import active_config
from configuration import configurations

try:
    from camera.snapshot import concurrent_snapshot
except ImportError:
    def concurrent_snapshot(ts):
        print('SERI SERVER: PICAMERA NOT AVAILABLE')

from events.events import *
from serial_interface import serial_interface


def execute_command(handler, main, sub=''):
    event_handler.execute_command(handler, main, sub)


class SerialEventHandler:

    def __init__(self, *args, **kwargs):
        super(SerialEventHandler, self).__init__(*args, **kwargs)

        self.handler = None

    def execute_command(self, handler, main, sub):
        if self.handler:
            handler.notify()
            return
        else:
            self.handler = handler  # Semaphore set to prevent another event interrupting.

        serial_interface.send_message(main, sub)

    def reply(self, reply):
        self.handler.notify(reply=reply)
        self.handler = None


event_handler = SerialEventHandler()


def proximity_alarm(sub):
    alarm_status = sub == ON
    print("SERI SERVER: Alarm status received: ", alarm_status)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H:%M:%S")

    serial_interface.send_message(PROXIMITY_ALARM, ON if alarm_status else OFF)

    if active_config.get_config_item(configurations.ALARM):

        if active_config.get_config_item(configurations.PICTURE_MODE):
            concurrent_snapshot(timestamp)

        http_requests.notify_alarm(alarm_status, timestamp)


def reply_received(sub=''):
    event_handler.reply(sub)


def get_alarm_status(sub):
    reply_received(sub=sub)


def error():
    print('SERI SERVER: Error received')
    reply_received()


def event_notification(event):
    event_info = event.split(" ")

    if len(event_info) > 1:
        main, sub = event_info
        events[main](sub)
    else:
        events[event_info[0]]()


events = {
        PROXIMITY_ALARM: proximity_alarm,
        GET_ALARM_STATE: get_alarm_status,
        ERR: error,
    }
