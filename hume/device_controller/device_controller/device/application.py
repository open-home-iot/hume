import sys
import threading
import logging

from bottle import run, WSGIRefServer
from . import routes  # To load routes

LOGGER = logging.getLogger(__name__)


class MyServer(WSGIRefServer):
    """
    Thanks SO user Sepero for this one:
    https://stackoverflow.com/questions/11282218/bottle-web-framework-how-to-stop/19749945#19749945
    """

    def run(self, app):  # pragma: no cover
        """
        This is a copy from bottle.WSGIRefServer, only one line added.
        """
        from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
        from wsgiref.simple_server import make_server
        import socket

        class FixedHandler(WSGIRequestHandler):
            def address_string(self):  # Prevent reverse DNS lookups please.
                return self.client_address[0]

            def log_request(*args, **kw):
                if not self.quiet:
                    return WSGIRequestHandler.log_request(*args, **kw)

        handler_cls = self.options.get('handler_class', FixedHandler)
        server_cls = self.options.get('server_class', WSGIServer)

        if ':' in self.host:  # Fix wsgiref for IPv6 addresses.
            if getattr(server_cls, 'address_family') == socket.AF_INET:
                class server_cls(server_cls):
                    address_family = socket.AF_INET6

        srv = make_server(self.host, self.port, app, server_cls, handler_cls)
        self.srv = srv  # THIS IS THE ONLY CHANGE TO THE ORIGINAL CLASS METHOD!
        srv.serve_forever()

    def shutdown(self):  # ADD SHUTDOWN METHOD.
        self.srv.shutdown()
        # self.server.server_close()


server = MyServer(host='localhost', port=8081)


def start():
    """
    Starts up the HTTP listener.
    """

    def start_http_server():
        """
        Starts an HTTP server locally on port 8081.
        """
        run(server=server)  # Blocks!

    LOGGER.info("device listener start")

    # TODO well, what will be used to communicate with devices?
    thread = threading.Thread(target=start_http_server)
    thread.start()


def stop():
    """
    Stop the HTTP listener.
    """
    LOGGER.info("device listener stop")
    server.shutdown()
