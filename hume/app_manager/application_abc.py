from abc import ABCMeta, abstractmethod


class ApplicationABC(metaclass=ABCMeta):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def status(self):
        pass
