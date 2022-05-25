import json
import logging
import threading

from app.device.connection.gdci import GDCI
from app.device.connection.sim_specs import (
    BASIC_LED_CAPS,
    DEVICE_UUID_LED,
    DEVICE_UUID_AQUARIUM,
    DEVICE_UUIDS,
    AQUARIUM_CAPS
)
from app.device.models import Device
from app.device.connection import ble
from app.device.connection.defs import DeviceTransport, DeviceMessage


LOGGER = logging.getLogger(__name__)


def discovered_device(device_dict):
    return Device(device_dict["uuid"],
                  device_dict["name"],
                  DeviceTransport.SIM.value,
                  device_dict["uuid"].replace('-', ':'),
                  False)


def initial_states(capabilities: dict) -> dict:
    i = 0
    states = dict()
    for _ in capabilities["states"]:
        states[i] = 0
        i += 1

    return states


class SimConnection(GDCI):

    class DeviceEntry:

        def __init__(self, device: Device, capabilities: dict):
            self.device = device
            self.callback = lambda _device, msg_type, msg: \
                LOGGER.warning(f"no notify callback for device "
                               f"{_device.uuid[:4]}")
            self.current_states = initial_states(capabilities)

        def update_state(self, group_id: int, state_id: int):
            self.current_states[group_id] = state_id

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
        LOGGER.info("connecting to device")

        self.device_registry[device.uuid] = SimConnection.DeviceEntry(
            device, self._capabilities[device.uuid]
        )

        return True

    def disconnect(self, device: Device) -> bool:
        LOGGER.info(f"disconnecting device {device.uuid[:4]}")

        self.device_registry.pop(device.uuid)

        return True

    def disconnect_all(self) -> bool:
        LOGGER.info("disconnecting all devices")

        self.device_registry = dict()
        return True

    def send(self, msg: GDCI.Message, to: Device) -> bool:
        LOGGER.debug(f"sending device {to.uuid[:4]} message {msg.content}")

        if self.device_registry.get(to.uuid) is None:
            raise ConnectionError(f"device {to.uuid[:4]} is not connected")

        request_type = ble.get_request_type(msg.content)

        if request_type == DeviceMessage.CAPABILITY.value:
            daemon = threading.Thread(
                target=self.device_registry[to.uuid].callback,
                args=(to,
                      request_type,
                      json.dumps(self._capabilities[to.uuid])),
                daemon=True
            )
            daemon.start()

        elif request_type == DeviceMessage.ACTION_STATEFUL.value:
            self._handle_stateful_action(msg, to)

        elif request_type == DeviceMessage.ACTION_STATES.value:
            self._handle_action_states(to)

        return True

    def _handle_stateful_action(self, msg: GDCI.Message, device: Device):
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
            raise ValueError("device does not have that group ID and state")

        self.device_registry.get(device.uuid).update_state(group_id, state_id)

        # cast handling to avoid performing the response handling before
        # indicating that the message has been sent.
        daemon = threading.Thread(
            target=self.device_registry[device.uuid].callback,
            args=(device,
                  DeviceMessage.ACTION_STATEFUL.value,
                  f"{group_id}{state_id}".encode("utf-8")),
            daemon=True
        )
        daemon.start()

    def _handle_action_states(self, device: Device):
        cb = self.device_registry[device.uuid].callback
        for group_id, state_id in self.device_registry[
            device.uuid
        ].current_states.items():
            cb(device,
               DeviceMessage.ACTION_STATEFUL.value,
               f"{group_id}{state_id}".encode("utf-8"))

    def notify(self, callback: callable, device: Device):
        LOGGER.info("activating notify")
        self.device_registry[device.uuid].callback = callback

    def for_each(self, callback: callable):
        for _, device in self.device_registry.items():
            callback(device)
