from abc import abstractmethod


PRIMARY_KEY = 1


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
