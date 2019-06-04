import subprocess
import os

from .. import ApplicationABC


class HttpApplication(ApplicationABC):

    server_process = None

    def start(self):
        print("Starting HTTP application process")

        self.server_process = subprocess.Popen(['gunicorn',
                                                '--chdir', os.path.dirname(os.path.abspath(__file__)) + '/server',
                                                'http_django_server.wsgi'])

    def stop(self):
        if self.server_process.poll() is None:
            self.server_process.terminate()

    def status(self):
        pass
