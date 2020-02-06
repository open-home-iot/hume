from device_controller.utility.broker import Broker


STORAGE_SERVICE_RPC_QUEUE = "rpc_storage_service"

_broker: Broker


def initialize(broker):
    global _broker
    _broker = broker


def get_persistent_config(query):
    _broker.rpc_call(STORAGE_SERVICE_RPC_QUEUE, query)
