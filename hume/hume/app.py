import json
import logging

from app.abc import StartError
from app.device import DeviceApp, DeviceMessage
from app.device.models import Device
from app.hint import HintApp
from app.hint.defs import HintMessage
from util.storage import DataStore

LOGGER = logging.getLogger(__name__)


class Hume:

    def __init__(self, cli_args):
        self.cli_args = cli_args
        self.storage = DataStore()
        self.device_app = DeviceApp(cli_args, self.storage)
        self.hint_app = HintApp(cli_args, self.storage)

    def start(self):
        """Starts the HUME."""
        LOGGER.info("hume start")

        self.storage.start()

        self.device_app.pre_start()
        self.hint_app.pre_start()

        # Register callbacks prior to starting Apps in case of any
        # confirmation-type messages happen on connection establishment, or in
        # case of queued up messages from HINT.
        self.device_app.register_callback(self._on_device_message)
        self.hint_app.register_callback(self._on_hint_message)

        try:
            self.device_app.start()
            self.hint_app.start()
        except StartError:
            self.stop()
            raise RuntimeError("failed to start an app")

        self.device_app.post_start()
        self.hint_app.post_start()

    def stop(self):
        """Stops the HUME."""
        LOGGER.info("hume stop")

        self.device_app.pre_stop()
        self.hint_app.pre_stop()

        self.device_app.stop()
        self.hint_app.stop()

        self.device_app.post_stop()
        self.hint_app.post_stop()

    """
    Private
    """

    def _on_device_message(self, device: Device, msg_type: int, msg: bytearray):
        """
        Registered to be called by the Device app when a new message is
        received from a connected device.
        """
        LOGGER.debug("HUME handling device message")

        decoded_msg = json.loads(msg)

        if msg_type == DeviceMessage.CAPABILITY.value:
            LOGGER.info(f"device {device.uuid[:4]} sent capability response")
            capabilities = decoded_msg
            capabilities["identifier"] = device.uuid

            if self.hint_app.create_device(capabilities):
                LOGGER.info("device created in HINT successfully")

                # delete the old device entry and re-set with capability-
                # provided UUID. This is done since BLE devices cannot provide
                # UUID before capability response is gotten and are thus saved
                # with their address as their primary key prior to attach
                # success.
                self.storage.delete(device)
                new_device = Device(uuid=capabilities["uuid"],
                                    address=device.address,
                                    name=device.name,
                                    attached=True)
                self.storage.set(new_device)
            else:
                LOGGER.error("failed to create device in HINT")
                # Detach device to clean up after unsuccessful attach.
                self.device_app.detach(device)
                self.hint_app.attach_failure(device)

        elif msg_type == DeviceMessage.ACTION_STATEFUL.value:
            self.hint_app.action_response(device,
                                          HintMessage.ACTION_STATEFUL,
                                          {
                                              "group_id": int(decoded_msg[0]),
                                              "state_id": int(decoded_msg[1])
                                          })

        else:
            LOGGER.warning(f"got message from device {device.uuid[:4]} of an "
                           f"unknown type: {msg_type}, msg: {msg}")

    def _on_hint_message(self, msg_type, msg):
        """
        Registered to be called by the Hint app when a new message is received
        from HINT.
        """
        LOGGER.debug("HUME handling HINT message")

        if msg_type == HintMessage.DISCOVER_DEVICES.value:
            LOGGER.info("HINT requested device discovery")
            self.device_app.discover(self.hint_app.discovered_devices)

        elif msg_type == HintMessage.ATTACH.value:
            identifier = msg["identifier"]
            LOGGER.info(f"HINT requested device {identifier[:4]} to "
                        f"be attached")

            error = True
            device = self.storage.get(Device, identifier)
            if device is not None:
                if self.device_app.request_capabilities(device):
                    error = False

            if error:
                LOGGER.error(f"failed to attach device {identifier[:4]}")
                self.hint_app.attach_failure(Device(uuid=identifier))

        elif msg_type == HintMessage.DETACH.value:
            device_uuid = msg["device_uuid"]
            LOGGER.info(f"HINT requested detaching device {device_uuid[:4]}")
            device = self.storage.get(Device, device_uuid)
            if device is not None:
                self.device_app.detach(device)
            else:
                LOGGER.error(f"can't detach device {device_uuid[:4]}, "
                             f"does not exist")

        elif msg_type == HintMessage.UNPAIR.value:
            LOGGER.info("HINT requested unpairing, factory resetting HUME")
            self.device_app.reset()
            self.storage.delete_all()

        elif msg_type == HintMessage.ACTION_STATEFUL.value:
            device_uuid = msg.pop("device_uuid")
            LOGGER.info(f"HINT requested stateful action for device "
                        f"{device_uuid[:4]}")
            msg.pop("type")
            device = self.storage.get(Device, device_uuid)
            if device is not None:
                self.device_app.stateful_action(device, **msg)
            else:
                LOGGER.error("could not execute stateful action since device "
                             "does not exist")

        else:
            LOGGER.warning(f"got message from hint of an unknown type: "
                           f"{msg_type}, msg: {msg}")
