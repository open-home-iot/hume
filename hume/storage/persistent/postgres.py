import logging
import peewee


LOGGER = logging.getLogger(__name__)

PSQL_DB_NAME = "hume"

# TODO parameterize
PSQL_DB = peewee.PostgresqlDatabase(PSQL_DB_NAME,
                                    user="hume",
                                    password="password")


class PersistentModel(peewee.Model):
    """
    Base class for all persistent models.
    """

    class Meta:
        database = PSQL_DB


class PostgresProxy:
    """
    Handles the connection to the storage service for persistent storage.
    """

    def __init__(self):
        """"""
        LOGGER.debug("PostgresProxy __init__")

        self._db = PSQL_DB

    def start(self):
        """"""
        LOGGER.info("starting PostgresProxy")
        self._db.connect()

    def define_table(self, model):
        """
        Defines tables in the postgres DB.

        :param model: .
        """
        LOGGER.debug("PostgresProxy define tables")

        self._db.create_tables([model])
