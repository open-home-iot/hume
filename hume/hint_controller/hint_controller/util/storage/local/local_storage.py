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
