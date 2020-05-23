import logging

from device_controller.device.model import Device
from device_controller.util import storage
from device_controller.config import application as config

LOGGER = logging.getLogger(__name__)


def confirm_attach(message_content):
    """
    Called on HINT controller confirming an attached device.

    :param dict message_content:
    :return:
    """
    LOGGER.debug(f"confirm attach received: {message_content}")

    # Resolve device
    uuid = message_content["uuid"]
    device = storage.get(Device, uuid)
    LOGGER.debug(f"found device: {device}")

    # Mark device as attached
    device.attached = True
    storage.save(device)


def device_configuration(message_content):
    """
    Called on HINT controller forwarding a device's new configuration data.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"device configuration received: {message_content}")

    # Load into config application
    config.new_configuration(message_content["uuid"], message_content["config"])


def device_action(message_content):
    """
    Called on HINT controller forwarding a device action.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"device action received: {message_content}")

    # TODO forward action to the device


def sub_device_action(message_content):
    """
    Called on HINT controller forwarding a sub device action.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"sub device action received: {message_content}")

    # TODO forward action to the device
