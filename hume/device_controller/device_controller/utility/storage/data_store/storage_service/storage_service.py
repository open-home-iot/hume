from device_controller.utility.broker import Broker
from device_controller.utility.storage.data_store.storage_service.messages import \
    create_table_message, decode_response
from device_controller.utility.storage.definitions import DataModel


STORAGE_SERVICE_RPC_QUEUE = "rpc_storage_service"

# HTTP code corresponding to: Conflict
PERSISTENT_TABLE_ALREADY_DEFINED = 409


class StorageService:

    _broker: Broker
    _service_name: str

    def __init__(self, broker, service_name):
        self._broker = broker
        self._service_name = service_name

    def define_table(self, model_instance: DataModel):
        message = create_table_message(self._service_name, model_instance)

        # TODO call storage service to register tables
        #response = self._broker.rpc_call(STORAGE_SERVICE_RPC_QUEUE, message)

    def get_persistent_data(self, query):
        pass
