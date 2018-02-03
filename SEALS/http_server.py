from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from threading import Thread, Event

from SEALS.serial_interface.events import *
from SEALS.serial_interface import serial_interface


class HTTPRequestHandler(BaseHTTPRequestHandler):
    """

    """
    log_file = open('server.log', 'w')
    event = Event()

    def do_GET(self):
        """

        :return:
        """
        request_path = urlparse(self.path)

        if 'shutdown' in request_path.path:
            shutdown_thread = Thread(target=shutdown, args=(self,))
            shutdown_thread.daemon = True
            shutdown_thread.start()
        elif 'distance' in request_path.path:
            print("HTTP SERVER: Sending get distance command")
            serial_interface.execute_command(GET_DISTANCE)
            print("HTTP SERVER: Waiting for reply")
            # TODO look into Condition.wait_for(). Remember that max wait time should be defined to avoid deadlocks
            reply = serial_interface.get_reply_message()
            print("HTTP SERVER: Reply was: ", reply)

    def log_message(self, format, *args):
        """

        :param format:
        :param args:
        :return:
        """
        self.log_file.write("%s - - [%s] %s\n" %
                            (self.client_address[0],
                             self.log_date_time_string(),
                             format % args))


def shutdown(handler):
    """

    :param handler:
    :return:
    """
    handler.log_file.close()
    handler.server.shutdown()


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    """

    :param server_class:
    :param handler_class:
    :return:
    """
    server_address = ('', 8080)
    server = server_class(server_address, handler_class)
    server.serve_forever()


def notify_reply():
    """

    :return:
    """
    print("HTTP SERVER: Notified of reply")
    # TODO look into Condition.wait_for()


if __name__ == '__main__':
    serial_interface.start()
    run(handler_class=HTTPRequestHandler)
