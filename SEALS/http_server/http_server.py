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

        elif 'get_alarm_state' in request_path.path:
            print('HTTP SERVER: Got get alarm status command')
            serial_event_handler.execute_command(self, main=GET_ALARM_STATE)

            self.wait()
            print("HTTP SERVER: Reply was: ", self.reply)

        elif 'set_alarm_state' in request_path.path:
            main, sub = request_path.path.split('/')
            serial_event_handler.execute_command(self, main=SET_ALARM_STATE, sub=sub)

            self.wait()
            print('HTTP SERVER: Reply was: ', self.reply)

        else:
            print(request_path.path)


def shutdown(handler):
    handler.server.shutdown()


def start(server_address):
    server = HTTPServer(server_address, HTTPRequestHandler)
    print("HTTP SERVER: Starting HTTP server")
    server.serve_forever()
