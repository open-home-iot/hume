from abc import abstractmethod


class DataModel:

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
