import logging

from device_controller.utility.broker import Broker
from device_controller.utility.storage.data_store.storage_service.messages import \
    create_table_message
from device_controller.utility.storage.definitions import DataModel


STORAGE_SERVICE_RPC_QUEUE = "rpc_storage_service"

# HTTP code corresponding to: Conflict
PERSISTENT_TABLE_ALREADY_DEFINED = 409


LOGGER = logging.getLogger(__name__)


class StorageService:
    """
    Handles the connection to the storage service for persistent storage.
    """

    _broker: Broker
    _service_name: str

    def __init__(self, broker, service_name):
        """
        :param broker: HUME broker instance
        :param service_name: using service name
        """
        LOGGER.debug("StorageService __init__")

        self._broker = broker
        self._service_name = service_name

    def define_table(self, model_instance: DataModel):
        """
        Defines a table with the storage service.

        :param model_instance: instantiated data model
        """
        LOGGER.info("StorageService define table")

        message = create_table_message(self._service_name, model_instance)

        # TODO call storage service to register tables
        #response = self._broker.rpc_call(STORAGE_SERVICE_RPC_QUEUE, message)

        return PERSISTENT_TABLE_ALREADY_DEFINED

    def get_persistent_data(self, query):
        """
        Queries the storage service for persistent data.

        :param query:
        :return: persistent data according to query
        """
        LOGGER.info(f"StorageService get persistent data for {query}")
