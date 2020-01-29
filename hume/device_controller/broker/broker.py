import logging

from rabbitmq_client.client import RMQClient


class Broker:
    """
    The Broker provides both an internal (to the Python Process) and external
    (to the entire host) message dispatching capabilities.
    """
    internal_subscriptions = dict()

    rmq_client: RMQClient

    def __init__(self):
        """"""
        self.rmq_client = RMQClient(log_level=logging.INFO)

    def start(self):
        """
        Starts the Broker, initializing the RMQ client. Enables RPC client
        capabilities by default.
        """
        print("broker start")
        self.rmq_client.start()
        self.rmq_client.enable_rpc_client()

    def stop(self):
        """
        Stops the Broker, releasing its resources.
        """
        print("broker stop")

    def subscribe_global(self, topic, callback):
        """
        Subscribes to a RMQ topic using the RMQClient.

        :param str topic: topic to listen on
        :param callable callback: callback on message to the topic
        """
        self.rmq_client.subscribe(topic, callback)

    def subscribe_local(self, topic, callback):
        """
        Subscribes in the local python process to a topic.

        :param topic: topic to listen on
        :param callback: callback on message to the topic
        """
        subscriptions = self.internal_subscriptions.get(topic)

        if subscriptions is not None:
            # Exists, add callback to list of callbacks
            self.internal_subscriptions.update(
                {topic: subscriptions.append(callback)}
            )
        else:
            # Empty, create new list of callbacks
            self.internal_subscriptions[topic] = [callback]

    def enable_rpc_server(self, queue_name, callback):
        """
        Enables RPC requests by creating a queue with the provided name, this
        will ensure that messages sent to <queue_name> will result in an
        invocation of callback(message: bytes).

        :param queue_name: queue name of the RPC server
        :param callback: callback on message to the RPC queue
        """
        self.rmq_client.enable_rpc_server(queue_name, callback)

    def publish_global(self, topic, message):
        """
        Publishes a message on the given topic, using the RMQ client.

        :param str topic: topic to publish on
        :param bytes message: message to publish
        """
        self.rmq_client.publish(topic, message)

    def publish_local(self, topic, message):
        """
        Publishes a message on the given topic, using a process-local
        dictionary-mapping between topics and callbacks.

        :param str topic: topic to publish on
        :param str message:
        """
        subscriptions = self.internal_subscriptions.get(topic)

        if subscriptions is None:
            raise Exception("That subscription does not exist")
        else:
            for subscription in subscriptions:
                subscription(message)

