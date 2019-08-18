from .. import ApplicationABC


class LogApplication(ApplicationABC):

    def start(self):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :return: N/A
        """

        pass

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
