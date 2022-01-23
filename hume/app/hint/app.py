import json
import logging
import sys

import pika

from rabbitmq_client import (
    RMQConsumer,
    RMQProducer,
    QueueParams,
    ConsumeParams
)

from app.device.models import Device
from defs import CLI_BROKER_IP_ADDRESS, CLI_BROKER_PORT, CLI_HUME_UUID
from util.storage import DataStore
from app.abc import App
from app.hint.models import HumeUser, BrokerCredentials, HintAuthentication

LOGGER = logging.getLogger(__name__)


class HintMessage:
    DISCOVER_DEVICES = 0
    ATTACH_DEVICE = 1
    ACTION_STATEFUL = 2
    UNPAIR = 3
    DETACH = 4


class HintApp(App):
    HINT_MASTER_COMMAND_QUEUE = "hint_master"

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
            self.cli_args.get(CLI_HUME_UUID), durable=True
        )
        self._hint_queue_params = QueueParams(
            HintApp.HINT_MASTER_COMMAND_QUEUE, durable=True
        )
        self._consumer = RMQConsumer()
        self._producer = RMQProducer()

        self._registered_callback = lambda msg_type, msg: LOGGER.warning(
            "no registered callback to propagate HINT message to"
        )

    """
    App LCM
    """

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

        # Consumer from the HUME's input command queue.
        self._consumer.consume(ConsumeParams(self._on_hint_message),
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

    """
    Public
    """

    def register_callback(self, callback):
        """
        Registers a callback with the device app to be called when a device has
        sent the HUME a message.

        :param callback: callable(int, dict)
        :return:
        """
        LOGGER.info("registering callback")
        self._registered_callback = callback

    def discovered_devices(self, devices: [Device]):
        """
        Forwards the input devices to HINT.
        """
        LOGGER.info("sending discover devices result to HINT")

        message = {
            "type": HintMessage.DISCOVER_DEVICES,
            "content": [{"name": device.name,
                         "identifier": device.uuid} for device in devices]
        }

        self._publish(message)

    def create_device(self, device_spec):
        pass

    def attach_failure(self, device):
        pass

    def action_response(self):
        pass

    def unpair(self):
        pass

    """
    Private
    """

    def _on_hint_message(self, message: bytes):
        """
        Called when the consumer which monitors the HUME's message queue
        received a message.
        """
        LOGGER.debug("received HINT message")
        decoded_message = json.loads(message.decode('utf-8'))
        self._registered_callback(decoded_message["type"], decoded_message)

    def _publish(self, message: dict):
        """Publish to the HINT message queue."""
        self._producer.publish(self._encode_hint_command(message),
                               queue_params=self._hint_queue_params)

    def _encode_hint_command(self, message: dict):
        """Formats a HINT message."""
        message["uuid"] = self.cli_args.get(CLI_HUME_UUID)
        return json.dumps(message)
