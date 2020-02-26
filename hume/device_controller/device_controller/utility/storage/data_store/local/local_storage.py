import logging


LOGGER = logging.getLogger(__name__)


class LocalStorage:

    def __init__(self):
        LOGGER.debug("LocalStorage __init__")

        self._data_dict = dict()

    def define_storage(self, models):
        LOGGER.debug("Defining local storage")

        for model in models:
            # Keys based on ids of instances
            self._data_dict[model.__name__] = dict()

        LOGGER.debug(f"Current local storage state: {self._data_dict}")
