import logging

from device import connection


LOGGER = logging.getLogger(__name__)


def discover_devices(on_devices_discovered):
    """
    Entrypoint for a device discovery procedure.

    :param on_devices_discovered: callable([Device]) will be called when one
                                  or more devices have been discovered
    """
    LOGGER.info("device discovery procedure started")

    connection.discover(on_devices_discovered)


def attach_device(device_address, callback):
    """
    Attaches a device to the HUME, meaning it can be communicated with from now
    on. Attaching a device will mean that:

     1. The device can send HUME events
     2. HUME can issue the device commands (such as actions)
     3. HUME will start to regularly check the device connectivity through
        heartbeat checks

    :param device_address: address of the device to attach, a connection handle
    :param callback: callable to be called when attach has been attempted,
        should follow the format: callable(bool, Device)
    :return: True on success
    """
    pass