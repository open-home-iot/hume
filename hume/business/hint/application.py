from operations.log.application import Logger, LOG_LEVEL_INFO, LOG_LEVEL_DEBUG
from lib.application_base import ApplicationABC


class Hint(ApplicationABC):

    application_name = 'Hint'

    logger: Logger = None  # Typed for ease-of-access.

    def start(self, *args, logger=None, **kwargs):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :param logger: logging application
        :return: N/A
        """
        self.logger = logger

        self.logger.write_to_log(
            LOG_LEVEL_DEBUG, self.application_name, "Started."
        )

    def stop(self):
        """
        Stop lifecycle hook for all applications following the simple
        lifecycle management pattern. This hook should ensure that all resources
        related to this application are released.

        :return: N/A
        """
        self.logger.write_to_log(
            LOG_LEVEL_DEBUG, self.application_name, "Stopped."
        )

    def status(self):
        """
        Status information for the application. This function should
        return information about the application's current state.

        :return: N/A
        """
        pass
