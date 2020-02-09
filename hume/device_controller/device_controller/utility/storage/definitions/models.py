from abc import ABC, abstractmethod

from device_controller.utility.storage.definitions import PrimaryKey, \
    ForeignKey, OneToOne


def is_key(field_value):
    if isinstance(field_value, PrimaryKey):
        return True
    elif isinstance(field_value, ForeignKey):
        return field_value.is_primary_key
    elif isinstance(field_value, OneToOne):
        return True
    else:
        return False


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

    def key(self):
        fields = vars(self.__class__)
        for k, v in fields.items():
            if is_key(v):
                return k

        raise KeyError("There is no unique key for the model: {}"
                       .format(self.__class__.__name__))
