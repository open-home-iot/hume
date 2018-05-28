import json

from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.parse import urlparse

from events.events import *
from serial_interface import serial_event_handler
from http_server.http_requests import get_config
from configuration.active_config import active_config
from configuration.active_config import update_config
from configuration.configurations import *


class HTTPRequestHandler(BaseHTTPRequestHandler, EventThread):
    reply = 'unset'

    def notify(self, reply='error'):
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

        elif 'configuration_change' in request_path.path:
            print('HTTP SERVER: Got new configuration update')
            query = urlparse(self.path).query
            query_components = dict(qc.split('=') for qc in query.split('&'))

            update_config(query_components)

        elif 'get_alarm_state' in request_path.path:
            print('HTTP SERVER: Got get alarm status command')
            serial_event_handler.execute_command(self, main=GET_ALARM_STATE)

            self.wait(timeout=5.0)
            print("HTTP SERVER: Reply was: ", self.reply)

            if self.reply == 'unset':
                self.send_response(500)
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()
                json_dump = json.dumps({'alarm_state': True if self.reply == ON else False})
                self.wfile.write(json_dump.encode('utf-8'))

        else:
            print("HTTP SERVER: Path not found: ", request_path.path)


def shutdown(handler):
    handler.server.shutdown()


def start(server_address):
    # Get config first since the config determines if reporting should be carried outwards.
    print("HTTP SERVER: Getting configuration")
    config = get_config()
    active_config.set_config_item(ALARM, config['alarm_state'])
    active_config.set_config_item(PICTURE_MODE, config['picture_mode'])

    print("HTTP SERVER: Starting HTTP server")
    server = HTTPServer(server_address, HTTPRequestHandler)
    server.serve_forever()
