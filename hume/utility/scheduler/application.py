from lib.application_base import ApplicationABC
from operations.log.application import Logger, LOG_LEVEL_INFO


class Scheduler(ApplicationABC):

    application_name = 'Scheduler'

    logger: Logger = None

    def start(self, *args, logger=None, **kwargs):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :param logger: logging application
        :return: N/A
        """
        self.logger = logger

        self.logger.write_to_log(
            LOG_LEVEL_INFO, self.application_name, "Started."
        )

    def stop(self):
        """
        Stop lifecycle hook for all applications following the simple
        lifecycle management pattern. This hook should ensure that all resources
        related to this application are released.

        :return: N/A
        """
        self.logger.write_to_log(
            LOG_LEVEL_INFO, self.application_name, "Stopped."
        )

    def status(self):
        """
        Status information for the application. This function should
        return information about the application's current state.

        :return: N/A
        """
        pass
