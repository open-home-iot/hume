import json
import logging

from app.abc import StartError
from app.device import DeviceApp, DeviceMessage
from app.device.models import Device
from app.hint import HintApp, HintMessage
from app.hint.models import HintAuthentication
from util.storage import DataStore

LOGGER = logging.getLogger(__name__)


class Hume:

    def __init__(self, cli_args):
        self.cli_args = cli_args
        self.storage = DataStore()
        self.device = DeviceApp(cli_args, self.storage)
        self.hint = HintApp(cli_args, self.storage)

    def start(self):
        """Starts the HUME."""
        LOGGER.info("Hume start")

        self.storage.start()

        self.device.pre_start()
        self.hint.pre_start()

        # Register callbacks prior to starting Apps in case of any
        # confirmation-type messages happen on connection establishment, or in
        # case of queued up messages from HINT.
        self.device.register_callback(self._on_device_message)
        self.hint.register_callback(self._on_hint_message)

        try:
            self.device.start()
            self.hint.start()
        except StartError:
            self.stop()
            raise RuntimeError("failed to start an app")

        self.device.post_start()
        self.hint.post_start()

    def stop(self):
        """Stops the HUME."""
        LOGGER.info("Hume stop")

        self.device.pre_stop()
        self.hint.pre_stop()

        self.device.stop()
        self.hint.stop()

        self.device.post_stop()
        self.hint.post_stop()

    """
    Private
    """

    def _on_device_message(self, device, msg_type, msg):
        """
        Registered to be called by the Device app when a new message is
        received from a connected device.
        """
        LOGGER.debug("HUME handling device message")

        if msg_type == DeviceMessage.CAPABILITY:
            LOGGER.info(f"device {device.uuid[:4]} sent capability response")
            capabilities = json.loads(msg)
            capabilities["identifier"] = device.uuid

            if self.hint.create_device(capabilities):
                LOGGER.info("device created in HINT successfully")

                # Update the device entry, set correct uuid. UUID is gotten
                # from capabilities, non-attached devices may have their
                # address set to the UUID field.
                self.storage.delete(device)
                new_device = Device(uuid=capabilities["uuid"],
                                    address=device.address,
                                    name=device.name,
                                    attached=True)
                self.storage.set(new_device)
            else:
                LOGGER.error("failed to create device in HINT")
                # Detach device to clean up after unsuccessful attach.
                self.device.detach(device)
                self.hint.attach_failure(device)

        elif msg_type == DeviceMessage.ACTION_STATEFUL:
            pass

        else:
            LOGGER.warning(f"got message from device {device.uuid[:4]} of an "
                           f"unknown type: {msg_type}, msg: {msg}")

    def _on_hint_message(self, msg_type, msg):
        """
        Registered to be called by the Hint app when a new message is received
        from HINT.
        """
        LOGGER.debug("HUME handling HINT message")

        if msg_type == HintMessage.DISCOVER_DEVICES:
            LOGGER.info("HINT requested device discovery")
            self.device.discover(self.hint.discovered_devices)

        elif msg_type == HintMessage.ATTACH:
            identifier = msg["identifier"]
            LOGGER.info(f"HINT requested device {identifier[:4]} to "
                        f"be attached")

            error = True
            device = self.storage.get(Device, identifier)
            if device is not None:
                if self.device.request_capabilities(device):
                    error = False

            if error:
                LOGGER.error(f"failed to attach device {identifier[:4]}")
                self.hint.attach_failure(Device(uuid=identifier))

        elif msg_type == HintMessage.DETACH:
            device_uuid = msg["device_uuid"]
            LOGGER.info(f"HINT requested detaching device {device_uuid[:4]}")
            device = self.storage.get(Device, device_uuid)
            if device is not None:
                self.device.detach(device)
            else:
                LOGGER.error(f"can't detach device {device_uuid[:4]}, "
                             f"does not exist")

        elif msg_type == HintMessage.UNPAIR:
            LOGGER.info("HINT requested unpairing, factory resetting HUME")
            self.device.reset()
            self.storage.delete_all()

        elif msg_type == HintMessage.ACTION_STATEFUL:
            device_uuid = msg.pop("device_uuid")
            LOGGER.info(f"HINT requested stateful action for device "
                        f"{device_uuid[:4]}")
            msg.pop("type")
            device = self.storage.get(Device, device_uuid)
            if device is not None:
                self.device.stateful_action(device, **msg)
            else:
                LOGGER.error("could not execute stateful action since device "
                             "does not exist")

        else:
            LOGGER.warning(f"got message from hint of an unknown type: "
                           f"{msg_type}, msg: {msg}")
