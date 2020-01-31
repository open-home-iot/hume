from device_controller.procedures.handler import ProcedureHandler
from device_controller.utility.broker import Broker


DEVICE_CONTROLLER_QUEUE = "device_controller"


class RPCHandler:

    broker: Broker
    procedure_handler: ProcedureHandler

    def __init__(self, broker=None, procedure_handler=None):
        self.broker = broker
        self.procedure_handler = procedure_handler

    def start(self):
        self.broker.enable_rpc_server(
            DEVICE_CONTROLLER_QUEUE,
            "pass"
        )

    def stop(self):
        pass
