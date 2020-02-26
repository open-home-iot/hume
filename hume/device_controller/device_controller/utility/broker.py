import logging

from rabbitmq_client.client import RMQClient


LOGGER = logging.getLogger(__name__)


class Broker:
    """
    HUME specific broker

    The Broker provides both an internal (to the Python Process) and external
    (to the entire host) message dispatching capabilities.
    """

    def __init__(self):
        """"""
        LOGGER.debug("Broker __init__")

        self._internal_subscriptions = dict()
        self._rmq_client = RMQClient(log_level=logging.INFO)

    def start(self):
        """
        Starts the Broker, initializing the RMQ client. Enables RPC client
        capabilities by default.
        """
        LOGGER.info("Broker start")

        self._rmq_client.start()
        self._rmq_client.enable_rpc_client()

    def stop(self):
        """
        Stops the Broker, releasing its resources.
        """
        LOGGER.info("Broker stop")

        self._rmq_client.stop()

    def subscribe_global(self, topic, callback):
        """
        Subscribes to a RMQ topic using the RMQClient.

        callback(message: bytes)

        :param str topic: topic to listen on
        :param callable callback: callback on message to the topic
        """
        LOGGER.info(f"Broker subscribe_global to {topic}")

        self._rmq_client.subscribe(topic, callback)

    def subscribe_local(self, topic, callback):
        """
        Subscribes in the local python process to a topic.

        callback(message: str)

        :param str topic: topic to listen on
        :param callable callback: callback on message to the topic
        """
        LOGGER.info(f"Broker subscribe_local to {topic}")

        subscriptions = self._internal_subscriptions.get(topic)

        if subscriptions is not None:
            # Exists, add callback to list of callbacks
            self._internal_subscriptions.update(
                {topic: subscriptions.append(callback)}
            )
        else:
            # Empty, create new list of callbacks
            self._internal_subscriptions[topic] = [callback]

    def publish_global(self, topic, message):
        """
        Publishes a message on the given topic, using the RMQ client.

        :param str topic: topic to publish on
        :param bytes message: message to publish
        """
        LOGGER.info(f"Broker publish_global to {topic}")

        self._rmq_client.publish(topic, message)

    def publish_local(self, topic, message):
        """
        Publishes a message on the given topic, using a process-local
        dictionary-mapping between topics and callbacks.

        :param str topic: topic to publish on
        :param str message:
        """
        LOGGER.info(f"Broker publish_local to {topic}")

        subscriptions = self._internal_subscriptions.get(topic)

        if subscriptions is None:
            raise Exception("That subscription does not exist")
        else:
            for subscription in subscriptions:
                subscription(message)

    def enable_rpc_server(self, queue_name, callback):
        """
        Enables RPC requests by creating a queue with the provided name, this
        will ensure that messages sent to <queue_name> will result in an
        invocation of callback(message: bytes).

        Callback must return bytes.

        :param str queue_name: queue name of the RPC server
        :param callable callback: callback on message to the RPC queue
        """
        LOGGER.info(f"Broker enable_rpc_server {queue_name}")

        self._rmq_client.enable_rpc_server(queue_name, callback)

    def rpc_call(self, receiver, message):
        """
        Sends a synchronous RPC call to the receiver queue name.

        :param str receiver: receiver queue name for the RPC call
        :param bytes message: message to send to the receiver
        :return bytes answer: answer to RPC call operation
        """
        LOGGER.info(f"Broker rpc_call to {receiver}")

        return self._rmq_client.rpc_call(receiver, message)
