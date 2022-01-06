import json
import logging

import storage

from device.connection.gci import GCI
from device.connection.sim.specs import BASIC_LED_CAPS, DEVICE_UUID_LED
from device.models import Device, DeviceAddress
from device.connection import messages
from device.request_handler import (
    capability_response,
    heartbeat_response,
    stateful_action_response
)
from defs import DeviceRequest, CLI_DEVICE_TRANSPORT
from util import get_arg

LOGGER = logging.getLogger(__name__)


def discovered_device(device_dict):
    return Device(name=device_dict["name"],
                  # simulated devices have no address, change format to differ
                  # between UUID and address.
                  address=device_dict["uuid"].replace('-', ':'),
                  uuid=device_dict["uuid"])


class SimConnection(GCI):

    def __init__(self):
        super().__init__()
        # device.uuid -> Device
        self.device_registry = dict()
        self._capabilities = {
            DEVICE_UUID_LED: BASIC_LED_CAPS,
        }

    def discover(self, on_devices_discovered):
        LOGGER.info("starting device discovery")
        unattached_devices = self._unattached_devices
        for device in unattached_devices:

            # Do not try to create devices that already exist (multiple
            # discoveries)
            existing_device = storage.get(DeviceAddress, device.address)
            if existing_device is not None:
                continue

            device_address = DeviceAddress(
                transport=get_arg(CLI_DEVICE_TRANSPORT),
                address=device.address,
                uuid=device.uuid
            )
            storage.save(device_address)
            device = Device(
                uuid=device.uuid,
                address=device.address,
                name=device.name
            )
            storage.save(device)

        if len(unattached_devices) > 0:
            LOGGER.info(f"found {len(unattached_devices)} devices")
            on_devices_discovered(unattached_devices)

    @property
    def _unattached_devices(self) -> [Device]:
        # Ok for now, needs to be changed when new device types are added to
        # the sim.
        if len(self.device_registry) == 0:
            return [discovered_device(BASIC_LED_CAPS)]

        return []

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

        request_type = messages.get_request_type(msg.content)

        if request_type == DeviceRequest.CAPABILITY:
            capability_response(device, json.dumps(BASIC_LED_CAPS))

        elif request_type == DeviceRequest.HEARTBEAT:
            heartbeat_response(device)

        elif request_type == DeviceRequest.ACTION_STATEFUL:
            self._handle_stateful_action(msg, device)

        return True

    def _handle_stateful_action(self, msg: GCI.Message, device: Device):
        if device.uuid == DEVICE_UUID_LED:
            pass
        else:
            raise ValueError("what device was that?")

        # Verify msg content actually is an action from the spec
        decoded_msg = msg.content.decode('utf-8')
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
            LOGGER.debug(f"states list of found states contained state: {state}")

        if len(states) != 1:
            LOGGER.error("device does not have that group ID and state")
            return

        success = True
        stateful_action_response(
            device, f"{group_id}{state_id}{success}".encode("utf-8")
        )

    def notify(self, callback: callable, device: Device):
        # No need to implement, send all messages to 'incoming_message' for
        # now.
        ...

    def for_each(self, callback: callable):
        for _, device in self.device_registry.items():
            callback(device)
