from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from threading import Thread
from SEALS.serial_interface import serial_interface


class HTTPRequestHandler(BaseHTTPRequestHandler):
    log_file = open('server.log', 'w')

    def do_GET(self):
        """ Parses the request path and performs the appropriate action """
        request_path = urlparse(self.path)

        if 'shutdown' in request_path.path:
            shutdown_thread = Thread(target=shutdown, args=(self,))
            shutdown_thread.daemon = True
            shutdown_thread.start()

        print(request_path)

    def log_message(self, format, *args):
        self.log_file.write("%s - - [%s] %s\n" %
                            (self.client_address[0],
                             self.log_date_time_string(),
                             format % args))


def shutdown(handler):
    """ SHUTTING THE SERVER DOWN """
    handler.log_file.close()
    handler.server.shutdown()


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    """ RUNNING THE SERVER """
    server_address = ('', 8080)
    server = server_class(server_address, handler_class)
    server.serve_forever()


if __name__ == '__main__':
    serial_interface.start()
    run(handler_class=HTTPRequestHandler)
