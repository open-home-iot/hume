import os

from datetime import datetime

from .. import ApplicationABC
from .defs import *


def now():
    return "{}{}{}".format(
        "[", datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "]"
    )


class LogApplication(ApplicationABC):

    application_name = 'LogApplication'

    log_directory = ''  # Initialized during start()
    master_log = 'hume.log'

    def start(self, args=None):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :param args: arguments intended for an application.
        :return: N/A
        """
        self.log_directory = \
            os.path.dirname(os.path.abspath(__file__)) + '/logfiles/'

        self.clear_logs(args)
        self.create_log(self.master_log)

    def stop(self):
        """
        Stop lifecycle hook for all applications following the simple
        lifecycle management pattern. This hook should ensure that all resources
        related to this application are released.

        :return: N/A
        """

        pass

    def status(self):
        """
        Status information for the logging application. This function should
        return information about the application's current state.

        :return: N/A
        """

        pass

    def clear_logs(self, args):
        """
        Clears any previously existing logs, if the '--clear-logs' argument
        was provided upon startup.

        :param args: arguments intended for an application.
        :return:     N/A
        """

        if args.clear_logs:
            log_files = os.listdir(self.log_directory)

            filtered_log_files = [log_file for log_file in log_files
                                  if '.log' in log_file]

            for log_file in filtered_log_files:
                print("Clearing log file: %s" % log_file)
                os.remove(self.log_directory + '/' + log_file)

    def create_log(self, log):
        """
        Creates a log file with the specified name in the 'log' parameter. If
        the log file already exists, it will not be re-created, but appended to.

        :param log: name of the log file to be created
        :return:    N/A
        """

        if '.log' not in log:
            raise NameError("Please end log file names with '.log'")

        operation = 'w'

        if os.path.exists(self.log_directory + log):
            operation = 'a'

        with open(self.log_directory + log, operation) as log:

            if operation == 'a':
                statement = "\nCONTINUED %s \n" % now()
            else:
                statement = "CREATED %s \n" % now()

            log.write(statement)

    def write_to_log(self, level, tag, message, log=None):
        """
        Writes to a log file.

        :param level:   determined if 'INFO', 'WARNING', or 'ERROR' should be
                        displayed next to the log entry.
        :param tag:     tag of the logging entity, to differentiate log entries
                        from one another.
        :param message: message content of the logging action.
        :param log:     optional argument to choose which EXISTING log to write
                        to. If left blank, the master log 'hume.log' is chosen.
                        If supplying a log file name, the call MUST be preceded
                        by a call to create_log(<log file name>)
        :return:
        """
        if log is None:
            log = self.master_log

        if not os.path.exists(self.log_directory + log):
            raise FileNotFoundError(log + " does not exist. You need to create"
                                          "it before attempting to write to it")

        with open(self.log_directory + log, 'a') as log:
            log.write("{} - {} {}: {}\n".format(
                now(), LOG_LEVEL_TAGS[level], tag, message)
            )
