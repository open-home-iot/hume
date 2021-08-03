"""
Designed as glue between the GCI implementer and callers, since callers are
calling discovery from a synchronous context.
"""


import logging

from device.connection.application import _gci_implementer

LOGGER = logging.getLogger(__name__)


def discover(on_devices_discovered):
    """
    Interface function for the discovery action of the GCI.
    """
    LOGGER.info("connection interface calling for a device discovery")

    _gci_implementer.instance.discover(
        on_devices_discovered)
