from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.parse import urlparse

from events.events import *
from serial_interface import serial_event_handler


class HTTPRequestHandler(BaseHTTPRequestHandler, EventThread):
    reply = None

    def notify(self, reply='busy'):
        self.reply = reply
        self.event.set()

    def do_GET(self):
        self.event = Event()
        request_path = urlparse(self.path)

        if 'shutdown' in request_path.path:
            print("HTTP SERVER: Got shutdown command")
            shutdown_thread = Thread(target=shutdown, args=(self,))
            shutdown_thread.daemon = True
            shutdown_thread.start()

        elif 'get_alarm_status' in request_path.path:
            print('HTTP SERVER: Got get alarm status command')
            serial_event_handler.execute_command(self, GET_ALARM_STATUS)

            self.wait()
            print("HTTP SERVER: Reply was: ", self.reply)

        elif 'set_alarm_state_on' in request_path.path:
            print('HTTP SERVER: Got set alarm state command')
            serial_event_handler.execute_command(self, SET_ALARM_STATE)

            self.wait()
            print('HTTP SERVER: Reply was: ', self.reply)

        elif 'set_alarm_state_off' in request_path.path:
            print('HTTP SERVER: Got set alarm state command')
            # TODO extend execute command to handle multiple args for main/sub
            serial_event_handler.execute_command(self, SET_ALARM_STATE)

            self.wait()
            print('HTTP SERVER: Reply was: ', self.reply)


def shutdown(handler):
    handler.server.shutdown()


def start(server_address):
    server = HTTPServer(server_address, HTTPRequestHandler)
    print("HTTP SERVER: Starting HTTP server")
    server.serve_forever()
