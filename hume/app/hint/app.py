import logging
import sys

import pika

from rabbitmq_client import (
    RMQConsumer,
    RMQProducer,
    QueueParams,
    ConsumeParams
)

from defs import CLI_BROKER_IP_ADDRESS, CLI_BROKER_PORT, CLI_HUME_UUID
from util.storage import DataStore
from app.abc import App
from app.hint.models import HumeUser, BrokerCredentials, HintAuthentication

LOGGER = logging.getLogger(__name__)


class HintApp(App):

    def __init__(self, cli_args, storage: DataStore):
        super().__init__()
        self.cli_args = cli_args
        self.storage = storage

        self._conn_params = pika.ConnectionParameters(
            host=self.cli_args.get(CLI_BROKER_IP_ADDRESS),
            port=self.cli_args.get(CLI_BROKER_PORT),
            virtual_host='/'
        )
        self._hume_queue_params = QueueParams(
            f"{self.cli_args.get(CLI_HUME_UUID)}", durable=True
        )
        self._consumer = RMQConsumer()
        self._producer = RMQProducer()

    def pre_start(self):
        LOGGER.info("Hint pre_start")
        self.storage.register(HumeUser)
        self.storage.register(BrokerCredentials)
        self.storage.register(HintAuthentication)

        hume_user = self.storage.get(HumeUser, None)
        if hume_user is None:
            pair()  # first time startup, call pairing procedure
            LOGGER.info("first time startup succeeded")
        else:
            if not login_to_hint(hume_user):
                sys.exit(1)  # not recoverable right now

            LOGGER.info("startup succeeded")
            # Skip checking broker credentials

    def start(self):
        LOGGER.info("Hint start")

        # Fetch broker credentials
        broker_credentials = self.storage.get(BrokerCredentials, None)

        if broker_credentials is not None:
            credentials = pika.PlainCredentials(broker_credentials.username,
                                                broker_credentials.password)
        else:
            # Default fallback to avoid exceptions at this stage
            credentials = pika.PlainCredentials('guest', 'guest')

        self._conn_params.credentials = credentials
        self._consumer.connection_parameters = self._conn_params
        self._producer.connection_parameters = self._conn_params

        self._consumer.start()
        self._producer.start()

        # Initialize command lib with producer instance
        command_library.init(self._producer)

        # Consumer from the HUME's input command queue.
        self._consumer.consume(ConsumeParams(command_handler.incoming_command),
                               queue_params=self._hume_queue_params)

    def post_start(self):
        LOGGER.info("Hint post_start")

    def pre_stop(self):
        LOGGER.info("Hint pre_stop")

    def stop(self):
        LOGGER.info("Hint stop")
        self._consumer.stop()
        self._producer.stop()

    def post_stop(self):
        LOGGER.info("Hint post_stop")
