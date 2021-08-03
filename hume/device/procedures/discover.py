import logging

from device import connection


LOGGER = logging.getLogger(__name__)


def discover(on_devices_discovered=None):
    """Entrypoint for a device discovery procedure"""
    devices = connection.discover(on_devices_discovered=on_devices_discovered)
