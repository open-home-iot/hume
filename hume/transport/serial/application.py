from .. import ApplicationABC


class SerialApplication(ApplicationABC):

    application_name = 'SerialApplication'

    def start(self, args=None, utility_applications=None):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :param args: arguments intended for an application.
        :param utility_applications: a list of all utility applications that
                                     the serial application is allowed to
                                     use.
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
