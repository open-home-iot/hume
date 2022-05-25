from __future__ import annotations

from typing import Union

from util.storage import Model
from app.device.connection.defs import DeviceTransport


class Device(Model):
    persistent = True
    key = "uuid"

    def __init__(self,
                 uuid: str,
                 name: str,
                 transport: Union[DeviceTransport.BLE.value,
                                  DeviceTransport.SIM.value],
                 address: str,
                 attached: bool):
        self.uuid = uuid
        self.name = name
        self.transport = transport
        self.address = address
        self.attached = attached

    @classmethod
    def decode(cls,
               uuid: str = None,
               name: str = None,
               transport: str = None,
               address: str = None,
               attached: str = None) -> Device:
        return cls(uuid,
                   name,
                   DeviceTransport(transport).value,
                   address,
                   bool(int(attached)))
