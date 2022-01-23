import json
import logging

from rabbitmq_client import RMQProducer, QueueParams

from util import get_arg
from defs import CLI_HUME_UUID, HintMessage

LOGGER = logging.getLogger(__name__)

HINT_MASTER_COMMAND_QUEUE = "hint_master"
_producer: RMQProducer
_hint_queue_params = QueueParams(HINT_MASTER_COMMAND_QUEUE, durable=True)


def init(producer_instance):
    """
    :type producer_instance: rabbitmq_client.RMQProducer
    """
    global _producer
    _producer = producer_instance


def encode_hint_command(command: dict):
    """Formats a HINT command."""
    command["uuid"] = get_arg(CLI_HUME_UUID)
    return json.dumps(command)


def publish(command: dict):
    """Publish to the HINT master queue."""
    _producer.publish(encode_hint_command(command),  # noqa
                      queue_params=_hint_queue_params)


def devices_discovered(devices):
    """
    This is just a forward of what was returned by DC since the messages look
    exactly the same.

    :type devices: [Device]
    """
    LOGGER.info("sending discover devices result to HINT")

    command = {
        "type": HintMessage.DISCOVER_DEVICES,
        "content": [{"name": device.name,
                     "identifier": device.uuid} for device in devices]
    }

    publish(command)


def attach_failure(device):
    """
    Indicates to HINT a failure to attach the input device.

    :param device: Device
    """
    LOGGER.info("sending attach failure to HINT")

    message = {
        "type": HintMessage.ATTACH_DEVICE,
        "content": {
            "identifier": device.uuid,
            "success": False,
        },
    }

    publish(message)


def action_response(device, action_type, info: dict):
    """
    Indicates to HINT the response to an action request.

    :param device:
    :param action_type:
    :param info: information about the action
    """
    LOGGER.info("sending action response to HINT")

    message = {
        "type": action_type,
        "device_uuid": device.uuid,
        "content": info
    }

    publish(message)
