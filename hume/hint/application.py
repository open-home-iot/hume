import logging
import pika
import sys

from rabbitmq_client import (
    RMQConsumer,
    RMQProducer,
    ConsumeParams,
    QueueParams
)

from hint.models import (
    HumeUser,
    BrokerCredentials,
    HintAuthentication
)
from hint import (
    command_handler
)
from hint.procedures import command_library
from hint.procedures.hint_connectivity import login_to_hint, pair
from util import get_arg, storage as storage
from defs import (
    CLI_HUME_UUID,
    CLI_BROKER_IP_ADDRESS,
    CLI_BROKER_PORT,
)

LOGGER = logging.getLogger(__name__)

_consumer = RMQConsumer()
_hume_queue_params: QueueParams

_producer = RMQProducer()


def model_init():
    """
    Initialize models.
    """
    LOGGER.info("model-init")
    storage.register(HumeUser)
    storage.register(BrokerCredentials)
    storage.register(HintAuthentication)


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")

    hume_user = storage.get(HumeUser, None)
    if hume_user is None:
        pair()  # first time startup, call pairing procedure
        LOGGER.info("first time startup succeeded")
    else:
        if not login_to_hint(hume_user):
            sys.exit(1)  # not recoverable right now

        LOGGER.info("startup succeeded")
        # Skip checking broker credentials


def start():
    """
    Starts up the hint application.
    """
    LOGGER.info("hint start")

    # Fetch broker credentials
    broker_credentials = storage.get(BrokerCredentials, None)

    if broker_credentials is not None:
        credentials = pika.PlainCredentials(broker_credentials.username,
                                            broker_credentials.password)
    else:
        # Default fallback to avoid exceptions at this stage
        credentials = pika.PlainCredentials('guest', 'guest')
    conn_params = pika.ConnectionParameters(host=get_arg(
                                                CLI_BROKER_IP_ADDRESS
                                            ),
                                            port=get_arg(CLI_BROKER_PORT),
                                            virtual_host='/',
                                            credentials=credentials)

    global _consumer, _producer, _hume_queue_params
    _consumer = RMQConsumer(connection_parameters=conn_params)
    _producer = RMQProducer(connection_parameters=conn_params)

    _consumer.start()
    _producer.start()

    # Initialize command lib with producer instance
    command_library.init(_producer)

    # Consumer from the HUME's input command queue.
    _hume_queue_params = QueueParams(f"{get_arg(CLI_HUME_UUID)}", durable=True)
    _consumer.consume(ConsumeParams(command_handler.incoming_command),
                      queue_params=_hume_queue_params)


def stop():
    """
    Stop the hint application.
    """
    LOGGER.info("hint stop")
    _consumer.stop()
    _producer.stop()
