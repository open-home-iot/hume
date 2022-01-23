import logging

from util import storage

from device import connection
from device.models import Device, DeviceAddress, DeviceHealth
from device.procedures.request_library import capability
from device.request_handler import incoming_message
from hint.procedures.command_library import attach_failure

LOGGER = logging.getLogger(__name__)


def discover_devices(on_devices_discovered):
    """
    Entrypoint for a device discovery procedure.

    :param on_devices_discovered: callable([Device]) will be called when one
                                  or more devices have been discovered
    """
    LOGGER.info("device discovery procedure started")

    connection.discover(on_devices_discovered)


def detach_device(uuid):
    """
    Detaches a device from the HUME, deleting all data associated with it.

    :param uuid: UUID of the device
    """
    LOGGER.info(f"detaching device {uuid}, all its data is deleted")

    device = storage.get(Device, uuid)
    connection.disconnect(device)

    address = storage.get(DeviceAddress, device.address)
    health = storage.get(DeviceHealth, device.uuid)
    storage.delete(device)
    storage.delete(address)
    storage.delete(health)
