import logging


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

        self._data_dict[model.__name__] = dict()

        LOGGER.debug(f"Current local storage state: {self._data_dict}")

    def save(self, obj):
        """
        Save an object to local storage dict.

        :param obj: object to save
        """
        LOGGER.debug("saving to in memory dictionary")

        self._data_dict[obj.__class__.__name__][obj.local_key_field()] = obj
        LOGGER.debug(f"Current local storage state: {self._data_dict}")
