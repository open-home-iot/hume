import subprocess
import os
import threading

from . import server_handler
from . import defs
from .. import ApplicationABC


class HttpApplication(ApplicationABC):

    application_name = 'HttpApplication'
    server_process = None

    def start(self, args=None, utility_applications=None):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :param args: arguments intended for an application.
        :param utility_applications: a list of all utility applications that
                                     the http application is allowed to
                                     use.
        :return: N/A
        """

        gunicorn_root_path = \
            os.path.dirname(os.path.abspath(__file__)) + '/server/'
        print("Gunicorn root %s" % gunicorn_root_path)

        def prestart_clean():
            if os.path.isfile(
                    gunicorn_root_path + defs.GUNICORN_ACCESS_LOGFILE
            ):
                print("Removing Gunicorn access logfile")
                os.remove(gunicorn_root_path + defs.GUNICORN_ACCESS_LOGFILE)
            if os.path.isfile(
                    gunicorn_root_path + defs.GUNICORN_ERROR_LOGFILE
            ):
                print("Removing Gunicorn error logfile")
                os.remove(gunicorn_root_path + defs.GUNICORN_ERROR_LOGFILE)

            print("Prestart clean done")

        prestart_clean()

        print("Starting HTTP application process")
        self.server_process = subprocess.Popen(
            ['gunicorn',
             '--chdir', gunicorn_root_path,
             '--access-logfile', defs.GUNICORN_ACCESS_LOGFILE,
             '--error-logfile', defs.GUNICORN_ERROR_LOGFILE,
             'http_django_server.wsgi']
        )

        thread = threading.Thread(target=server_handler.start, daemon=True)
        thread.start()

    def stop(self):
        """
        Stop lifecycle hook for all applications following the simple
        lifecycle management pattern. This hook should ensure that all resources
        related to this application are released.

        :return: N/A
        """

        if self.server_process.poll() is None:
            self.server_process.terminate()

    def status(self):
        """
        Status information for the application. This function should
        return information about the application's current state.

        :return: N/A
        """
        pass
