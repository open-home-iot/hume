from abc import ABC, abstractmethod


class ServerBase(ABC):
    """
    Base class for servers.
    """

    @abstractmethod
    def start(self):
        """
        Starts the server and sets up resources it needs.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Stops the server and ensures resources are released.
        """
        pass
