import subprocess
import os
import psutil

from utility.log.application import LogApplication, \
    LOG_LEVEL_INFO, LOG_LEVEL_ERROR

from transport.http_listener import defs
from lib.application_base import ApplicationABC


class HttpListener(ApplicationABC):

    application_name = 'HttpListener'

    log_application: LogApplication = None  # Typed for ease-of-access.

    gunicorn_root_path = ''
    server_process = None

    def start(self, args=None, utility_applications=None):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :param args: arguments intended for an application.
        :param utility_applications: a dict of all utility applications that
                                     the application is allowed to
                                     use.
        :return: N/A
        """
        self.log_application = utility_applications[defs.APPL_UTIL_LOG]

        self.check_for_started_servers()

        self.gunicorn_root_path = os.path.dirname(os.path.abspath(__file__))

        self.log_application.write_to_log(
            LOG_LEVEL_INFO,
            self.application_name,
            "Gunicorn root path: {}".format(self.gunicorn_root_path)
        )

        self.clear_gunicorn_logs(args)

        self.server_process = subprocess.Popen(
            ['gunicorn',
             '--chdir', self.gunicorn_root_path,
             '--access-logfile', defs.GUNICORN_ACCESS_LOGFILE,
             '--error-logfile', defs.GUNICORN_ERROR_LOGFILE,
             'http_django_server.wsgi']
        )

        self.log_application.write_to_log(
            LOG_LEVEL_INFO, self.application_name, "Started."
        )

    def stop(self):
        """
        Stop lifecycle hook for all applications following the simple
        lifecycle management pattern. This hook should ensure that all resources
        related to this application are released.

        :return: N/A
        """

        if self.server_process.poll() is None:
            self.server_process.terminate()

        self.log_application.write_to_log(
            LOG_LEVEL_INFO, self.application_name, "Stopped."
        )

    def status(self):
        """
        Status information for the application. This function should
        return information about the application's current state.

        :return: N/A
        """
        pass

    def clear_gunicorn_logs(self, args):
        if args.clear_logs:
            if os.path.isfile(
                    self.gunicorn_root_path + defs.GUNICORN_ACCESS_LOGFILE
            ):
                os.remove(
                    self.gunicorn_root_path + defs.GUNICORN_ACCESS_LOGFILE
                )
            if os.path.isfile(
                    self.gunicorn_root_path + defs.GUNICORN_ERROR_LOGFILE
            ):
                os.remove(
                    self.gunicorn_root_path + defs.GUNICORN_ERROR_LOGFILE
                )

    def check_for_started_servers(self):
        gunicorn_pids = []

        # Process all processes
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
            try:
                # If a process was started by python, inspect it
                if 'python' in proc.info['name']:

                    # Inspect the command line arguments, this will show if the
                    # python process started a gunicorn program
                    for cmd in proc.info['cmdline']:

                        # Found one! Add the PID to the list of PIDs so that the
                        # user can terminate the process manually
                        if 'gunicorn' in cmd:
                            gunicorn_pids.append(proc.pid)
                            break

            except psutil.NoSuchProcess:
                pass

        if len(gunicorn_pids) > 0:

            # Write to log which PID needs to be terminated
            self.log_application.write_to_log(
                LOG_LEVEL_ERROR,
                self.application_name,
                "An instance of the HTTP application's http_listener exists already, "
                "please kill the process before re-starting. The following "
                "process IDs need to be terminated: {}".format(gunicorn_pids)
            )

            raise SystemError("An instance of the HTTP application's http_listener "
                              "exists already, please kill the process before "
                              "re-starting. See the 'hume.log' for more "
                              "information.")
