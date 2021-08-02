import logging
import copy

from storage.definitions import SINGLETON


LOGGER = logging.getLogger(__name__)


class LocalStorage:
    """
    Handles the cache of dynamic information which is lost on shutdown.
    """

    def __init__(self):
        """"""
        LOGGER.debug("LocalStorage __init__")

        self._data_dict = dict()

    def define_storage(self, model):
        """
        Defines space in the local storage dict for input model.

        :param model:
        """
        LOGGER.debug("Defining local storage")

        if model.local_key_field() == SINGLETON:
            # No need for initialization, just need the table key.
            self._data_dict[model.__name__] = None
        else:
            self._data_dict[model.__name__] = dict()

        LOGGER.debug(f"Current local storage state: {self._data_dict}")

    def save(self, obj):
        """
        Save an object to local storage dict.

        :param obj: object to save
        """
        LOGGER.debug("saving to in memory dictionary")

        local_key_field = obj.local_key_field()

        if local_key_field == SINGLETON:
            self._data_dict[obj.__class__.__name__] = obj
        else:
            table = self._data_dict[obj.__class__.__name__]
            table.update({getattr(obj, local_key_field): obj})

        LOGGER.debug(f"resulting local storage state: {self._data_dict}")

    def get(self, cls, key):
        """
        Get a single object matching the provided key. Will always check local
        storage only as it should be up to date with persistent storage.

        :param cls: class
        :param key: key
        :return: class object matching key or None
        """
        LOGGER.debug("getting object")

        table = self._data_dict[cls.__name__]
        LOGGER.debug(f"table contents: {table}")

        if cls.local_key_field() == SINGLETON:
            # Just one object exists.
            return copy.deepcopy(table)

        return copy.copy(table.get(key))

    def get_all(self, cls):
        """
        Get all objects of the provided class.

        :param cls:
        :return:
        """
        LOGGER.debug(f"getting all object of model: {cls}")

        if cls.local_key_field() == SINGLETON:
            return copy.copy(self._data_dict[cls.__name__])
        else:
            table = copy.deepcopy(self._data_dict[cls.__name__])
            return table.values()

    def save_all(self, data):
        """
        Sets all objects in the data list to the local storage dict.

        :param data: list of objects to save
        """
        LOGGER.debug("setting all objects in input list")

        for obj in data:
            self.save(obj)

    def delete(self, obj):
        """
        Removes the object from both local and persistent storage.

        :param obj:
        """
        LOGGER.debug("deleting object from local storage")

        if obj.local_key_field() == SINGLETON:
            # Can't pop the whole table...
            self._data_dict[obj.__class__.__name__] = None
        else:
            table = self._data_dict[obj.__class__.__name__]
            table.pop(getattr(obj, obj.local_key_field()))

        LOGGER.debug(f"resulting local storage state: {self._data_dict}")
