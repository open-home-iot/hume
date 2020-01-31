import logging

from abc import ABC, abstractmethod

from rabbitmq_client.client import RMQClient


class Dispatch(ABC):
    """
    Interface for dispatch receivers.
    """
    @abstractmethod
    def dispatch(self, message: dict):
        """
        Handles a message dispatch.

        :param dict message: message to dispatch
        """
        pass


class Broker:
    """
    The Broker provides both an internal (to the Python Process) and external
    (to the entire host) message dispatching capabilities.
    """
    internal_subscriptions = dict()
    registered_dispatchers = dict()

    rmq_client: RMQClient

    def __init__(self):
        """"""
        self.rmq_client = RMQClient(log_level=logging.INFO)

    def start(self):
        """
        Starts the Broker, initializing the RMQ client. Enables RPC client
        capabilities by default.
        """
        print("utility start")
        self.rmq_client.start()
        self.rmq_client.enable_rpc_client()

    def stop(self):
        """
        Stops the Broker, releasing its resources.
        """
        print("utility stop")
        self.rmq_client.stop()

    def subscribe_global(self, topic, callback):
        """
        Subscribes to a RMQ topic using the RMQClient.

        callback(message: bytes)

        :param str topic: topic to listen on
        :param callable callback: callback on message to the topic
        """
        self.rmq_client.subscribe(topic, callback)

    def subscribe_local(self, topic, callback):
        """
        Subscribes in the local python process to a topic.

        callback(message: str)

        :param str topic: topic to listen on
        :param callable callback: callback on message to the topic
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

        Callback must return bytes.

        :param str queue_name: queue name of the RPC server
        :param callable callback: callback on message to the RPC queue
        """
        self.rmq_client.enable_rpc_server(queue_name, callback)

    def rpc_call(self, receiver, message):
        """
        Sends a synchronous RPC call to the receiver queue name.

        :param str receiver: receiver queue name for the RPC call
        :param bytes message: message to send to the receiver
        :return bytes answer: answer to RPC call operation
        """
        return self.rmq_client.rpc_call(receiver, message)

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

    def register_dispatch(self, receiver, identifier):
        """
        Receivers that register must implement the dispatch interface:

        receiver.dispatch(message: dict)

        :param receiver: receiver of future dispatches
        :param identifier: identifier for this dispatch
        """
        assert issubclass(receiver.__class__, Dispatch)

        self.registered_dispatchers[identifier] = receiver

    def dispatch(self, to, message):
        """
        Dispatches a message to a registered dispatch.

        :param to: specify which registered dispatch shall get the message
        :param dict message: message to dispatch
        """
        assert to in self.registered_dispatchers.keys()

        self.registered_dispatchers[to].dispatch(message)
