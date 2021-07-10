import logging
import json

from rabbitmq_client import (
    RMQConsumer,
    RMQProducer,
    ConsumeParams,
    QueueParams
)

from hc_dispatch.command_handler import incoming_command
from util import get_arg
from hc_defs import CLI_HUME_UUID


LOGGER = logging.getLogger(__name__)

_consumer = RMQConsumer()
_dc_command_queue_params: QueueParams

_producer = RMQProducer()
_hc_command_queue_params: QueueParams


"""
This module is the starting point of the dc_dispatch application, responsible
for registering callbacks for various HUME internal comm. types.
"""


def model_init():
    """
    Initialize models.
    """
    LOGGER.info("model-init")


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")


def start():
    """
    Starts the dc_dispatch application
    """
    LOGGER.info("hc dc_dispatch start")
    global _dc_command_queue_params, _hc_command_queue_params
    _dc_command_queue_params = QueueParams(
        f"{get_arg(CLI_HUME_UUID)}-dc-commands", durable=True
    )
    _hc_command_queue_params = QueueParams(
        f"{get_arg(CLI_HUME_UUID)}-hc-commands", durable=True
    )

    _consumer.start()
    _consumer.consume(
        ConsumeParams(incoming_command),
        queue_params=_hc_command_queue_params
    )
    _producer.start()


def stop():
    """
    Stops the dc_dispatch application
    """
    LOGGER.info("hc dc_dispatch stop")
    _consumer.stop()
    _producer.stop()


def forward_command_to_dc(command):
    """
    :type command: bytes
    """
    LOGGER.info("forwarding command to DC")

    _producer.publish(command, queue_params=_dc_command_queue_params)  # noqa


def dc_command(command_content):
    """
    Input must be possible to convert to valid JSON.

    :type command_content: dict
    """
    LOGGER.info("sending a command to DC")

    _producer.publish(
        json.dumps(command_content).encode('utf-8'),
        queue_params=_dc_command_queue_params  # noqa
    )
