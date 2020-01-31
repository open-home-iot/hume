from device_controller.procedures.handler import ProcedureHandler
from device_controller.utility.broker import Broker


class ConfigServer:

    broker: Broker
    procedure_handler: ProcedureHandler

    def __init__(self, broker=None,
                 procedure_handler=None,
                 on_config_event=None):
        self.broker = broker
        self.procedure_handler = procedure_handler
        self._on_config_event = on_config_event

    def start(self):
        pass

    def stop(self):
        pass
