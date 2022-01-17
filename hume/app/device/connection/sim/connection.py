import json
import logging

from defs import DeviceRequest
from ..gci import GCI
from .specs import (
    BASIC_LED_CAPS,
    DEVICE_UUID_LED,
    DEVICE_UUID_AQUARIUM,
    DEVICE_UUIDS,
    AQUARIUM_CAPS
)
from app.device.models import Device
from app.device.connection import messages
from app.device.defs import TRANSPORT_SIM

LOGGER = logging.getLogger(__name__)


def discovered_device(device_dict):
    return Device(uuid=device_dict["uuid"],
                  # simulated devices have no address, change format to differ
                  # between UUID and address.
                  transport=TRANSPORT_SIM,
                  address=device_dict["uuid"].replace('-', ':'),
                  name=device_dict["name"])


class SimConnection(GCI):

    def __init__(self):
        super().__init__()
        # device.uuid -> Device
        self.device_registry = dict()
        self._capabilities = {
            DEVICE_UUID_LED: BASIC_LED_CAPS,
            DEVICE_UUID_AQUARIUM: AQUARIUM_CAPS,
        }

    def discover(self, on_devices_discovered):
        LOGGER.info("starting device discovery")

        if len(self._unattached_devices) > 0:
            LOGGER.info(f"found {len(self._unattached_devices)} devices")
            on_devices_discovered(self._unattached_devices)

    @property
    def _unattached_devices(self) -> [Device]:
        return [discovered_device(self._capabilities[uuid])
                for uuid in DEVICE_UUIDS
                if uuid not in self.device_registry.keys()]

    def is_connected(self, device: Device) -> bool:
        return self.device_registry.get(device.uuid) is not None

    def connect(self, device: Device) -> bool:
        LOGGER.info(f"connecting to device {device.uuid}")

        self.device_registry[device.uuid] = device

        return True

    def disconnect(self, device: Device) -> bool:
        LOGGER.info(f"disconnecting device {device.uuid}")

        self.device_registry.pop(device.uuid)

        return True

    def disconnect_all(self) -> bool:
        LOGGER.info("disconnecting all devices")

        self.device_registry = dict()
        return True

    def send(self, msg: GCI.Message, device: Device) -> bool:
        LOGGER.debug(f"sending device {device.uuid} message {msg.content}")

        if self.device_registry.get(device.uuid) is None:
            raise ValueError(f"device {device.uuid} is not connected")

        request_type = messages.get_request_type(msg.content)

        if request_type == DeviceRequest.CAPABILITY:
            capability_response(device,
                                json.dumps(self._capabilities[device.uuid]))

        elif request_type == DeviceRequest.HEARTBEAT:
            heartbeat_response(device)

        elif request_type == DeviceRequest.ACTION_STATEFUL:
            self._handle_stateful_action(msg, device)

        return True

    def _handle_stateful_action(self, msg: GCI.Message, device: Device):
        if (device.uuid == DEVICE_UUID_LED or
                device.uuid == DEVICE_UUID_AQUARIUM):
            pass
        else:
            raise ValueError("that device does not support any stateful "
                             "actions...")

        # Verify msg content actually is an action from the spec
        decoded_msg = msg.content.decode("utf-8")
        capabilities = self._capabilities[device.uuid]
        group_id = int(decoded_msg[2])
        state_id = int(decoded_msg[3])

        states = []
        for state_group in capabilities["states"]:
            if state_group["id"] != group_id:
                continue

            LOGGER.debug(f"state group ID {state_group['id']} matched "
                         f"{group_id}, checking states of this group")

            states = [state for state in list(state_group.values())[1]
                      if list(state.values())[0] == state_id]

        for state in states:
            LOGGER.debug(f"states list of found states contained state: "
                         f"{state}")

        if len(states) != 1:
            LOGGER.error("device does not have that group ID and state")
            return

        success = True
        stateful_action_response(
            device, f"{group_id}{state_id}{success}".encode("utf-8")
        )

    def notify(self, callback: callable, device: Device):
        # TODO: implement before finishing refactoring
        ...

    def for_each(self, callback: callable):
        for _, device in self.device_registry.items():
            callback(device)
