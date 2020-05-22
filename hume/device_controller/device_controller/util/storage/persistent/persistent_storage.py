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

    def define_storage(self, model):
        """
        Defines cache space and tables in postgres.

        :param model: .
        """
        LOGGER.debug("Defining persistent storage")

        self._pg_proxy.define_table(model)

    def save(self, obj):
        """
        Save an object persistently.

        :param obj: object to save
        """
        LOGGER.debug("saving to database")

        obj.save()
