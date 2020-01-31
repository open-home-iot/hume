from device_controller.procedures.handler import ProcedureHandler
from device_controller.utility.broker import Broker
from device_controller.zigbee.server import DEVICE_EVENT_TOPIC


class ZigbeeHandler:

    broker: Broker
    procedure_handler: ProcedureHandler

    def __init__(self, broker=None, procedure_handler=None):
        self.broker = broker
        self.procedure_handler = procedure_handler

    def start(self):
        self.broker.subscribe_local(
            DEVICE_EVENT_TOPIC,
            ""
        )

    def stop(self):
        pass
