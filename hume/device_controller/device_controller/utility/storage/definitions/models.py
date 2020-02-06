from abc import ABC, abstractmethod


class DataModel(ABC):

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
