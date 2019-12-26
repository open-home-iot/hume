import pika
import signal

from operations.log.application import Logger, LOG_LEVEL_DEBUG, \
    LOG_LEVEL_WARNING


class Producer:
    """
    Class: Producer



    Terminology:

    Connection  -
    Channel     -
    IO loop     -
    """

    producer_name = "Producer"

    _connection: pika.SelectConnection
    _channel = None

    logger: Logger = None

    def __init__(self, logger=None):
        """
        Constructor for the Producer.

        :param logger: logging application
        """
        self.logger = logger

        self._closing = False

        signal.signal(signal.SIGTERM, self.terminate)

    def run(self):
        """
        Runs the Producer:
         1. connects to the configured RabbitMQ server
         2. creates a channel
         3. declares queue(s)
        """
        self.connect()
        self._connection.ioloop.start()

    def connect(self):
        """
        Sets up the connection to the RabbitMQ server.
        """
        self._connection = pika.SelectConnection(
            pika.ConnectionParameters(),
            on_open_callback=self.on_connected,
            on_close_callback=self.on_closed
        )

    def on_connected(self, _unused_connection):
        """
        Callback for completed connection.

        :param _unused_connection: pika connection object, already registered
                                   with the class instance, hence ignored.
        """
        self.logger.write_to_log(
            LOG_LEVEL_DEBUG, self.producer_name,
            "Opened connection to RabbitMQ server."
        )
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_closed(self, _unused_connection, reason):
        """
        Callback for closed connection.

        :param _unused_connection: pika connection object
        :param reason: reason for closed connection.
        """
        self.logger.write_to_log(
            LOG_LEVEL_DEBUG,
            self.producer_name,
            "Connection closed unexpectedly, reason: {}".format(reason)
        )

    def on_channel_open(self, new_channel):
        """
        Callback for opened channel.

        :param new_channel: created pika channel
        """
        self.logger.write_to_log(
            LOG_LEVEL_DEBUG, self.producer_name,
            "Opened channel to RabbitMQ server."
        )
        self._channel = new_channel
        self._channel.add_on_close_callback(self.on_channel_closed)
        self.logger.write_to_log(
            LOG_LEVEL_DEBUG, self.producer_name, "Started."
        )

    def on_channel_closed(self, _unused_channel, reason):
        """
        Callback for closed channel.

        :param _unused_channel: pika channel object
        :param reason: reason for closed channel
        """
        self.logger.write_to_log(
            LOG_LEVEL_DEBUG,
            self.producer_name,
            "Channel closed unexpectedly, reason: {}".format(reason)
        )

    def terminate(self, signum, frame):
        """
        Used to handle the SIGTERM signal, so that the consumer system can be
        shut down gracefully, even after an interrupt.

        :param signum: <see python docs>
        :param frame:  <see python docs>
        :return:       N/A
        """
        self.logger.write_to_log(
            LOG_LEVEL_WARNING, self.producer_name, "SIGTERM was received, stopping."
        )

        self.stop()

    def stop(self):
        """
        Stops the consumer by closing the connection and stopping the running
        IO loop.
        """
        self._connection.close()
        self._connection.ioloop.stop()
        self.logger.write_to_log(
            LOG_LEVEL_DEBUG, self.producer_name, "Stopped."
        )
