from .. import ApplicationABC


class StorageApplication(ApplicationABC):

    application_name = 'StorageApplication'

    def start(self, args=None):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :param args: arguments intended for an application.
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
        Status information for the application. This function should
        return information about the application's current state.

        :return: N/A
        """
        pass
