import logging
import peewee


LOGGER = logging.getLogger(__name__)

PSQL_DB_NAME = "hume"


class PersistentModel(peewee.Model):
    """
    Base class for all persistent models.
    """

    class Meta:
        database = peewee.PostgresqlDatabase(PSQL_DB_NAME)


class PostgresProxy:
    """
    Handles the connection to the storage service for persistent storage.
    """

    def __init__(self, user, password):
        """"""
        LOGGER.debug("PostgresProxy __init__")

        self._db = peewee.PostgresqlDatabase(PSQL_DB_NAME,
                                             user=user,
                                             password=password)

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

    def drop_tables(self, models):
        """
        Drops the input model's table.
        """
        self._db.drop_tables(models)
