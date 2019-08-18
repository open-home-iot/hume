from abc import ABCMeta, abstractmethod


class ApplicationABC(metaclass=ABCMeta):
    """
    Class: ApplicationABC

    Abstract Base Class for all applications of the HUME system. These abstract
    methods are intended to ease the way in which applications are started,
    stopped, and checked for status; in order to prevent applications all having
    different lifecycle management.
    """

    @abstractmethod
    def start(self):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :return: N/A
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Stop lifecycle hook for all applications following the simple
        lifecycle management pattern. This hook should ensure that all resources
        related to this application are released.

        :return: N/A
        """
        pass

    @abstractmethod
    def status(self):
        """
        Status information for the application. This function should
        return information about the application's current state.

        :return: N/A
        """
        pass
