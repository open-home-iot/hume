import logging

from .postgres import PostgresProxy


LOGGER = logging.getLogger(__name__)


class PersistentStorage:
    """
    Handles caching persistent storage items and interactions with Postgres
    through the peewee ORM.
    """

    def __init__(self):
        """"""
        LOGGER.debug("PersistentStorage __init__")

        self._pg_proxy = PostgresProxy()
        self._data_dict = dict()

    def define_storage(self, models):
        """
        Defines cache space and tables in postgres.

        :param models: .
        """
        LOGGER.debug("Defining persistent storage")

        for model in models:
            self._data_dict[model.__name__] = dict()

        self._pg_proxy.define_tables(models)

        LOGGER.debug(f"Current persistent storage state: {self._data_dict}")

    def set_obj(self, obj):
        """
        Set an object to persistent storage, will override existing objects and
        sync with the DB.

        :param obj: .
        """
        # Need to save first, don't want to accidentally end up in an
        # inconsistent state. Saving also gets the object a PK, needed to update
        # the dict.
        obj.save()  # Enough to sync with db and get a PK? Yes!
        self._data_dict[obj.__class__.__name__].update({obj.id: obj})

        LOGGER.debug(f"New persistent storage state: {self._data_dict}")
