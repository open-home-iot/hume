from abc import ABC, abstractmethod


class DataModel(ABC):

    singleton = False

    @abstractmethod
    def local(self):
        """
        :return: local attributes
        """
        ...

    @abstractmethod
    def persistent(self):
        """
        :return: persistent attributes
        """
        ...
