import sys
import logging

from util import get_arg
from defs import CLI_DEVICE_TRANSPORT, CLI_DEVICE_TRANSPORT_BLE


LOGGER = logging.getLogger(__name__)

if get_arg(CLI_DEVICE_TRANSPORT) == CLI_DEVICE_TRANSPORT_BLE:
    from device.connection.ble import interface
else:
    LOGGER.critical("could not resolve valid device transport")
    sys.exit(1)

discover = interface.discover
connect = interface.connect
disconnect = interface.disconnect
send = interface.send
notify = interface.notify
