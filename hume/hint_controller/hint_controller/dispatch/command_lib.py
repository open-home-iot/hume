import json
import logging

from hume_broker import broker

from hint_controller.dispatch import DEVICE_CONTROLLER_COMMAND_QUEUE
from hint_controller import defs


LOGGER = logging.getLogger(__name__)


def discover_devices(content):
    """
    :param content: message content to send
    :type content: str
    """
    LOGGER.debug("dispatching discover devices to DC")

    broker.command(
        DEVICE_CONTROLLER_COMMAND_QUEUE,
        json.dumps(
            {
                "type": defs.DISCOVER_DEVICES,
                "content": content
            }
        ).encode('utf-8')
    )
