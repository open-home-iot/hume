from lib.application_base import ApplicationABC


class HttpCommunicator(ApplicationABC):

    application_name = 'HttpCommunicator'

    def start(self, args=None, utility_applications=None):
        """
        Start lifecycle hook for the HTTP Communicator application, following
        the simple lifecycle management pattern.

        :param args: arguments intended for an application.
        :param utility_applications: a dict of all utility applications that
                                     the http application is allowed to
                                     use.
        :return: N/A
        """
        pass

    def stop(self):
        """
        Stop lifecycle hook for the HTTP Communicator application following the
        simple lifecycle management pattern. This hook should ensure that all
        resources related to this application are released.

        :return: N/A
        """
        pass

    def status(self):
        """
        Status information for the application. This function should
        return information about the application's current state.

        :return: status integer
        """
        pass
