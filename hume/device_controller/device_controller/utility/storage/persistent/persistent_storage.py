import logging

from .postgres import PostgresProxy


LOGGER = logging.getLogger(__name__)


class PersistentStorage:

    def __init__(self):
        LOGGER.debug("PersistentStorage __init__")

        self._pg_proxy = PostgresProxy()
        self._data_dict = dict()

    def define_storage(self, models):
        LOGGER.debug("Defining persistent storage")

        for model in models:
            self._data_dict[model.__name__] = dict()

        self._pg_proxy.define_tables(models)

        LOGGER.debug(f"Current persistent storage state: {self._data_dict}")
