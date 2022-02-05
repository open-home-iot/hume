import json
import logging

import pika
import requests

from rabbitmq_client import (
    RMQConsumer,
    RMQProducer,
    QueueParams,
    ConsumeParams
)

from app.device.models import Device
from defs import (
    CLI_BROKER_IP_ADDRESS,
    CLI_BROKER_PORT,
    CLI_HUME_UUID,
    CLI_HINT_PORT,
    CLI_HINT_IP_ADDRESS
)
from util.storage import DataStore
from app.abc import App, StartError
from app.hint.models import HumeUser, BrokerCredentials, HintAuthentication
from app.hint.defs import HintMessage

LOGGER = logging.getLogger(__name__)


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

        # TODO: TLS
        self._hint_url = (
            f"http://{self.cli_args.get(CLI_HINT_IP_ADDRESS)}:"
            f"{self.cli_args.get(CLI_HINT_PORT)}/hume-api/"
        )

        self._registered_callback = lambda msg_type, msg: LOGGER.warning(
            "no registered callback to propagate HINT message to"
        )

    """
    App LCM
    """

    def pre_start(self):
        LOGGER.info("hint app pre_start")
        self.storage.register(HumeUser)
        self.storage.register(BrokerCredentials)
        self.storage.register(HintAuthentication)

    def start(self):
        LOGGER.info("hint app start")

        # runs pairing, authentication, and getting updated broker credentials.
        # may raise StartErrors
        try:
            self._connect_and_sync_with_hint()
        except requests.exceptions.ConnectionError:
            LOGGER.critical("failed to sync with HINT")
            raise StartError("failed to sync with HINT")

        # Fetch broker credentials
        broker_credentials = self.storage.get(BrokerCredentials, None)
        if broker_credentials is not None:
            credentials = pika.PlainCredentials(broker_credentials.username,
                                                broker_credentials.password)
        else:
            raise StartError("no broker credentials available")

        self._conn_params.credentials = credentials
        self._consumer.connection_parameters = self._conn_params
        self._producer.connection_parameters = self._conn_params

        self._consumer.start()
        self._producer.start()

        # Consumer from the HUME's input command queue.
        self._consumer.consume(ConsumeParams(self._on_hint_message),
                               queue_params=self._hume_queue_params)

    def post_start(self):
        LOGGER.info("hint app post_start")

    def pre_stop(self):
        LOGGER.info("hint app pre_stop")

    def stop(self):
        LOGGER.info("hint app stop")
        self._consumer.stop()
        self._producer.stop()

    def post_stop(self):
        LOGGER.info("hint app post_stop")

    """
    Public
    """

    def register_callback(self, callback: callable):
        """
        Registers a callback with the device app to be called when a device has
        sent the HUME a message.

        callback: callable(int, dict)
        """
        LOGGER.info("registering callback")
        self._registered_callback = callback

    def discovered_devices(self, devices: [Device]):
        """
        Forwards the input devices to HINT.
        """
        LOGGER.info("sending discover devices result to HINT")

        message = {
            "type": HintMessage.DISCOVER_DEVICES.value,
            "content": [{"name": device.name,
                         "identifier": device.uuid} for device in devices]
        }
        self._publish(message)

    def create_device(self, device_spec: dict) -> bool:
        """
        Requests and HINT creates a device according to the input spec.
        """
        LOGGER.info("sending create device request")

        hint_auth = self.storage.get(HintAuthentication, None)
        response = requests.post(
            f"{self._hint_url}humes/"
            f"{self.cli_args.get(CLI_HUME_UUID)}/devices",
            json=device_spec,
            cookies={"sessionid": hint_auth.session_id,
                     "csrftoken": hint_auth.csrf_token},
            headers={"X-CSRFToken": hint_auth.csrf_token})

        if response.status_code == requests.codes.created:
            return True

        LOGGER.error("failed to create device")
        return False

    def attach_failure(self, device: Device):
        """Sends an attach failure notification to HINT."""
        LOGGER.info("sending attach failure to HINT")

        message = {
            "type": HintMessage.ATTACH.value,
            "content": {
                "identifier": device.uuid,
                "success": False,
            },
        }
        self._publish(message)

    def action_response(self,
                        device: Device,
                        action_type: HintMessage,
                        info: dict):
        """Sends an action response to HINT"""
        LOGGER.info("sending action response to HINT")

        message = {
            "type": action_type.value,
            "device_uuid": device.uuid,
            "content": info
        }
        self._publish(message)

    """
    Private
    """

    def _on_hint_message(self, message: bytes):
        """
        Called when the consumer which monitors the HUME's message queue
        receives a message.
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

    def _connect_and_sync_with_hint(self):
        """
        Connects to HINT and syncs its current status. If the HUME is new a
        HUME user instance is gotten and stored. If HUME exists then the
        existing HUME user instance is used to authenticate with HINT. If
        authentication is successful, then broker credentials are fetched. If
        that fetch fails we still attempt to start since old credentials may
        be stored. If we have no stored credentials then the start LCM method
        will raise a StartError.
        """
        LOGGER.info("connecting to HINT")

        hume_user = self._pair()
        # Should hopefully have a HUME user instance after pairing.
        if hume_user is None:
            raise StartError("no HumeUser instance available")
        self._authenticate(hume_user)
        # If authentication fails, we will never reach here since an exception
        # is raised.
        self._get_broker_credentials()

    def _pair(self) -> HumeUser:
        """
        Attempts to pair the HUME with HINT. In case the HUME UUID is not
        recognized by HINT, this method will raise a StartError.
        """
        # Start with an attempted pairing to see if the HUME is paired or
        # not.
        LOGGER.info("sending pairing request")
        response = requests.post(
            self._hint_url + "humes",
            json={"uuid": self.cli_args.get(CLI_HUME_UUID)}
        )

        if response.status_code == requests.codes.created:
            response_content = response.json()  # Contains login information.
            LOGGER.info(f"got hume user: {response_content}")
            user_info = response_content['hume_user']
            hume_user = HumeUser(username=user_info["username"],
                                 password=user_info["password"])
            self.storage.set(hume_user)

        elif response.status_code == requests.codes.conflict:
            # HUME already exists, so re-use current hume user.
            LOGGER.info("HUME already paired")

        elif response.status_code == requests.codes.forbidden:
            # Invalid HUME UUID
            raise StartError("HUME UUID is invalid")

        else:
            # Something else went wrong, perhaps HINT is unavailable, try
            # to continue startup anyway.
            LOGGER.warning("HINT could not interpret pairing")

        return self.storage.get(HumeUser, None)

    def _authenticate(self, hume_user: HumeUser):
        """
        Authenticates with HINT to be able to access privileged routes.
        """
        LOGGER.info("authenticating with HINT")

        response = requests.post(self._hint_url + "users/login",
                                 json={"username": hume_user.username,
                                       "password": hume_user.password})

        if response.status_code == requests.codes.ok:
            LOGGER.debug(f"got cookies {response.cookies}")
            session_id = response.cookies.get("sessionid")
            csrf_token = response.cookies.get("csrftoken")
            self.storage.set(HintAuthentication(session_id=session_id,
                                                csrf_token=csrf_token)
                             )
        else:
            # We could re-try but that mostly imposes complex handling of
            # something that happens very rarely. On start we can be a little
            # stricter and enforce that most operations go well, else restart.
            StartError("could not authenticate with HINT")

    def _get_broker_credentials(self):
        """
        Tries to fetch broker credentials from HINT. This happens on each
        start as a way of allowing the credentials to be changed at any point.
        HUME will then use updated credentials when restarted.
        """
        LOGGER.info("getting broker credentials")

        hint_auth = self.storage.get(HintAuthentication, None)
        response = requests.get(self._hint_url + "broker-credentials",
                                cookies={"sessionid": hint_auth.session_id})

        if response.status_code == requests.codes.ok:
            broker_credentials = response.json()
            LOGGER.debug(f"got broker credentials: {broker_credentials}")
            username = broker_credentials['username']
            password = broker_credentials['password']
            new_broker_credentials = BrokerCredentials(
                username=username,
                password=password,
            )
            self.storage.set(new_broker_credentials)
        else:
            LOGGER.warning("failed to fetch broker credentials")
