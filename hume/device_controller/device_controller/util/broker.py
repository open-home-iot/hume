import logging

from rabbitmq_client.client import RMQClient


LOGGER = logging.getLogger(__name__)

_internal_subscriptions = dict()
_rmq_client = RMQClient(log_level=logging.INFO)


def start():
    """
    Starts the Broker, initializing the RMQ client. Enables RPC client
    capabilities by default.
    """
    LOGGER.info("broker start")

    _rmq_client.start()
    _rmq_client.enable_rpc_client()


def stop():
    """
    Stops the Broker, releasing its resources.
    """
    LOGGER.info("broker stop")

    _rmq_client.stop()


def subscribe_global(topic, callback):
    """
    Subscribes to a RMQ topic using the RMQClient.

    callback(message: bytes)

    :param str topic: topic to listen on
    :param callable callback: callback on message to the topic
    """
    LOGGER.info(f"broker subscribe_global to {topic}")

    _rmq_client.subscribe(topic, callback)


def subscribe_local(topic, callback):
    """
    Subscribes in the local python process to a topic.

    callback(message: str)

    :param str topic: topic to listen on
    :param callable callback: callback on message to the topic
    """
    LOGGER.info(f"Broker subscribe_local to {topic}")

    subscriptions = _internal_subscriptions.get(topic)

    if subscriptions is not None:
        # Exists, add callback to list of callbacks
        _internal_subscriptions.update(
            {topic: subscriptions.append(callback)}
        )
    else:
        # Empty, create new list of callbacks
        _internal_subscriptions[topic] = [callback]


def publish_global(topic, message):
    """
    Publishes a message on the given topic, using the RMQ client.

    :param str topic: topic to publish on
    :param bytes message: message to publish
    """
    LOGGER.info(f"Broker publish_global to {topic}")

    _rmq_client.publish(topic, message)


def publish_local(topic, message):
    """
    Publishes a message on the given topic, using a process-local
    dictionary-mapping between topics and callbacks.

    :param str topic: topic to publish on
    :param str message:
    """
    LOGGER.info(f"broker publish_local to {topic}")

    subscriptions = _internal_subscriptions.get(topic)

    if subscriptions is None:
        raise Exception("That subscription does not exist")
    else:
        for subscription in subscriptions:
            subscription(message)


def enable_rpc_server(queue_name, callback):
    """
    Enables RPC requests by creating a queue with the provided name, this
    will ensure that messages sent to <queue_name> will result in an
    invocation of callback(message: bytes).

    Callback must return bytes.

    :param str queue_name: queue name of the RPC server
    :param callable callback: callback on message to the RPC queue
    """
    LOGGER.info(f"broker enable_rpc_server {queue_name}")

    _rmq_client.enable_rpc_server(queue_name, callback)


def rpc_call(receiver, message):
    """
    Sends a synchronous RPC call to the receiver queue name.

    :param str receiver: receiver queue name for the RPC call
    :param bytes message: message to send to the receiver

    :return bytes answer: answer to RPC call operation
    """
    LOGGER.info(f"broker rpc_call to {receiver}")

    return _rmq_client.rpc_call(receiver, message)
