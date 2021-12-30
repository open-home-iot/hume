import logging

import storage

from device import connection
from device.models import Device, DeviceAddress
from device.procedures.request_library import capability
from device.request_handler import incoming_message

LOGGER = logging.getLogger(__name__)


def discover_devices(on_devices_discovered):
    """
    Entrypoint for a device discovery procedure.

    :param on_devices_discovered: callable([Device]) will be called when one
                                  or more devices have been discovered
    """
    LOGGER.info("device discovery procedure started")

    connection.discover(on_devices_discovered)


def attach_device(identifier):
    """
    Attaches a device to the HUME, meaning it can be communicated with from now
    on. Attaching a device will mean that:

     1. The device can send HUME events
     2. HUME can issue the device commands (such as actions)
     3. HUME will start to regularly check the device connectivity through
        heartbeat checks

    :param identifier: ID for the device to attach, protocol specific
        depending on the connection type.
    """
    LOGGER.info("attach device procedure started")

    # works for BLE devices as well since the identifier in their case will
    # be the same address provided to HINT in the discovery response.
    device = storage.get(Device, identifier)
    if connection.is_connected(device):
        connection.disconnect(device)

    connected = connection.connect(device)

    if connected:
        connection.notify(incoming_message, device)
        # TODO: For other transport types, the capability response will
        #  probably be gotten synchronously right here.
        capability(device)

    # incoming_message will receive the device response, at least for BLE
    # devices where requests are not synchronous


def detach_device(uuid):
    """
    Detaches a device from the HUME, deleting all data associated with it.

    :param uuid: UUID of the device
    """
    device = storage.get(Device, uuid)
    connection.disconnect(device)

    address = storage.get(DeviceAddress, device.address)
    storage.delete(device)
    storage.delete(address)
