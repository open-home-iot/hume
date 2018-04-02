from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.parse import urlparse

from threading import Thread, Event

from event_handler.events import *
from event_handler import event_handler


class HTTPRequestHandler(BaseHTTPRequestHandler):
    reply = None
    event = None

    def do_GET(self):
        request_path = urlparse(self.path)
        print(request_path.path)
        self.event = Event()

        if 'shutdown' in request_path.path:
            shutdown_thread = Thread(target=shutdown, args=(self,))
            shutdown_thread.daemon = True
            shutdown_thread.start()

        elif 'distance' in request_path.path:
            print("HTTP SERVER: Sending get distance command")
            event_handler.execute_command(self, GET_DISTANCE)

            self.event.wait()
            print("HTTP SERVER: Reply was: ", self.reply)

    def resolve_wait(self, reply='Busy'):
        self.reply = reply
        self.event.set()


def shutdown(handler):
    event_handler.execute_command(handler, 'shutdown')
    handler.server.shutdown()


def start(server_address=('', 8000)):
    server = HTTPServer(server_address, HTTPRequestHandler)
    server.serve_forever()
