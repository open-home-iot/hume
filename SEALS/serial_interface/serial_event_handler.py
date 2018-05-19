from http_server import http_requests

from datetime import datetime

from configuration.active_config import active_config
from configuration import configurations

try:
    from camera.snapshot import concurrent_snapshot
except ImportError:
    def concurrent_snapshot():
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

    if alarm_status:
        if active_config.is_config_valid():
            serial_interface.send_message(PROXIMITY_ALARM, ON)

            if active_config.get_config_item(configurations.ALARM_STATE):
                timestamp = datetime.now().strftime("%Y_%m_%d_%H:%M:%S")

                if active_config.get_config_item(configurations.PICTURE_STATE):
                    concurrent_snapshot(timestamp)

                http_requests.notify_alarm(alarm_status, timestamp)

            else:
                serial_interface.send_message(SET_ALARM_STATE, OFF)
    else:
        serial_interface.send_message(PROXIMITY_ALARM, OFF)


def reply_received(sub):
    event_handler.reply(sub)


def get_alarm_status(sub):
    reply_received(sub)


def set_alarm_state(sub):
    reply_received(sub)


def event_notification(event):
    event_info = event.split(" ")

    main, sub = event_info
    events[main](sub)


events = {
        PROXIMITY_ALARM: proximity_alarm,
        GET_ALARM_STATE: get_alarm_status,
        SET_ALARM_STATE: set_alarm_state,
    }
