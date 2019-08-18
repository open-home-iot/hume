from utility.log.application import LogApplication
from utility.log.defs import LOG_LEVEL_INFO
from .. import ApplicationABC
from . import defs


class HintApplication(ApplicationABC):

    application_name = 'HintApplication'

    log_application: LogApplication = None  # Typed for ease-of-access.

    def start(self,
              args=None,
              utility_applications=None,
              transport_applications=None):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :param args: arguments intended for an application.
        :param utility_applications:   a dict of all utility applications that
                                       the hint application is allowed to
                                       use.
        :param transport_applications: a dict of all transport applications that
                                       the hint application is allowed to
                                       use.
        :return: N/A
        """
        self.log_application = utility_applications[defs.APPL_UTIL_LOG]

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
