from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.parse import urlparse

from threading import Thread, Event

from events.events import *
from events.event_handler import EventThread
from serial_interface import serial_event_handler


class HTTPRequestHandler(BaseHTTPRequestHandler, EventThread):
    reply = None

    def do_GET(self):
        self.event = Event()
        request_path = urlparse(self.path)

        if 'shutdown' in request_path.path:
            print("HTTP SERVER: Got shutdown command")
            shutdown_thread = Thread(target=shutdown, args=(self,))
            shutdown_thread.daemon = True
            shutdown_thread.start()

        elif 'distance' in request_path.path:
            print("HTTP SERVER: Sending get distance command")
            serial_event_handler.execute_command(self, GET_DISTANCE)

            self.wait()
            print("HTTP SERVER: Reply was: ", self.reply)

            # TODO extend to send the reponse back! (for more than this dummy test command though :-)

    def notify_reply(self, reply='Busy'):
        self.reply = reply
        self.event.set()


def shutdown(handler):
    serial_event_handler.execute_command(handler, 'shutdown')
    handler.server.shutdown()


def start(server_address):
    server = HTTPServer(server_address, HTTPRequestHandler)
    print("HTTP SERVER: Starting HTTP server")
    server.serve_forever()
