import logging
import copy

from typing import Type, Union

from util.storage.defs import Model, model_error, SINGLETON

LOGGER = logging.getLogger(__name__)


class LocalStorage:
    """
    Handles the cache of dynamic information which is lost on shutdown.
    """

    def __init__(self):
        self._data_dict = dict()

    def define_storage(self, model: Type[Model]):
        """
        Defines space in the local storage dict for input model.
        """
        LOGGER.debug("defining local storage")

        if model.__name__ in self._data_dict.keys():
            model_error(
                model.__name__,
                custom_message=f"model {model.__name__} is already registered"
            )

        if model.key == SINGLETON:
            # No need for initialization, just need the table key.
            self._data_dict[model.__name__] = None
        else:
            self._data_dict[model.__name__] = dict()

        LOGGER.debug(f"current local storage state: {self._data_dict}")

    def set(self, instance: Model):
        """
        Set an object to local storage's dict.
        """
        LOGGER.debug("saving to in memory dictionary")

        if instance.__class__.__name__ not in self._data_dict:
            model_error(instance.__class__.__name__)

        if instance.key == SINGLETON:
            self._data_dict[instance.__class__.__name__] = \
                copy.deepcopy(instance)
        else:
            table = self._data_dict[instance.__class__.__name__]
            table.update({getattr(instance, instance.key):
                          copy.deepcopy(instance)})

        LOGGER.debug(f"resulting local storage state: {self._data_dict}")

    def get(self, model: Type[Model], key: Union[str, SINGLETON]) -> Model:
        """
        Get the object in local storage's dict that resolves from 'key'.
        """
        LOGGER.debug("get local")

        if model.__name__ not in self._data_dict:
            model_error(model.__name__)

        tab = self._data_dict[model.__name__]

        if key == SINGLETON:
            return copy.deepcopy(tab)
        return copy.deepcopy(tab[key])

    def get_all(self, model: Type[Model]):
        """
        Get all instances of a model.
        """
        LOGGER.debug("get all local")
        if model.__name__ not in self._data_dict:
            model_error(model.__name__)

        if model.key == SINGLETON:
            return copy.deepcopy(self._data_dict[model.__name__])

        return [copy.deepcopy(value)
                for value in self._data_dict[model.__name__].values()]

    def delete(self, instance: Model):
        """Delete a model instance from the local storage's data dict."""
        LOGGER.debug("delete local")

        if instance.__class__.__name__ not in self._data_dict:
            model_error(instance.__class__.__name__)

        if instance.key == SINGLETON:
            self._data_dict[instance.__class__.__name__] = None
        else:
            self._data_dict[instance.__class__.__name__].pop(
                getattr(instance, instance.key))

        LOGGER.debug(f"resulting local storage state: {self._data_dict}")

    def delete_all(self, model=None):
        """Delete all data stored in the local data dict."""
        LOGGER.debug("delete all local")

        if model is not None:
            tab = self._data_dict[model.__name__]
            if isinstance(tab, dict):
                self._data_dict[model.__name__] = dict()
            else:
                self._data_dict[model.__name__] = None
            LOGGER.debug(f"resulting local storage state: {self._data_dict}")
            return

        for key in self._data_dict.keys():
            if isinstance(self._data_dict[key], dict):
                self._data_dict[key] = dict()
            else:
                self._data_dict[key] = None

        LOGGER.debug(f"resulting local storage state: {self._data_dict}")

    """
    Private
    """
