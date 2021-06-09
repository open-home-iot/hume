import logging
import json

from rabbitmq_client import (
    RMQConsumer,
    RMQProducer,
    ConsumeParams,
    QueueParams
)

from dc.dispatch.hc_command_handler import incoming_command
from dc.util.args import HUME_UUID, get_arg


LOGGER = logging.getLogger(__name__)

_consumer = RMQConsumer()
_dc_command_queue_params: QueueParams

_producer = RMQProducer()
_hc_command_queue_params: QueueParams


"""
This module is the starting point of the dispatch application, responsible for
registering callbacks for various HUME internal comm. types.
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
    Starts the dispatch application
    """
    LOGGER.info("dc dispatch start")
    global _dc_command_queue_params, _hc_command_queue_params
    _dc_command_queue_params = QueueParams(f"{get_arg(HUME_UUID)}-dc-commands",
                                           durable=True)
    _hc_command_queue_params = QueueParams(f"{get_arg(HUME_UUID)}-hc-commands",
                                           durable=True)

    _consumer.start()
    _consumer.consume(
        ConsumeParams(incoming_command),
        queue_params=_dc_command_queue_params
    )
    _producer.start()


def stop():
    """
    Stops the dispatch application
    """
    LOGGER.info("dc dispatch stop")
    _consumer.stop()
    _producer.stop()


def hc_command(command_content):
    """
    Input must be possible to convert to valid JSON.

    :type command_content: dict
    """
    _producer.publish(
        json.dumps(command_content).encode('utf-8'),
        queue_params=_hc_command_queue_params
    )
