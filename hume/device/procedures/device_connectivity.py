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


def attach_device(device_address):
    """
    Attaches a device to the HUME, meaning it can be communicated with from now
    on. Attaching a device will mean that:

     1. The device can send HUME events
     2. HUME can issue the device commands (such as actions)
     3. HUME will start to regularly check the device connectivity through
        heartbeat checks

    :param device_address: address of the device to attach, a connection handle
    """
    LOGGER.info("attach device procedure started")

    device_address = storage.get(DeviceAddress, device_address)
    device = storage.get(Device, device_address.uuid)
    if connection.is_connected(device):
        connection.disconnect(device)

    connected = connection.connect(device)

    if connected:
        connection.notify(incoming_message, device)
        # TODO: For other transport types, the capability response is gotten
        #  here
        capability(device)

    # incoming_message will receive the device response, at least for BLE
    # devices where requests are not synchronous
