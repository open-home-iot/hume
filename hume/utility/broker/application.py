from lib.application_base import ApplicationABC
from operations.log.application import Logger, LOG_LEVEL_INFO, LOG_LEVEL_DEBUG
from utility.broker.rabbitmq_handler.application import RabbitMQHandler


class Broker(ApplicationABC):

    application_name = 'Broker'

    logger: Logger = None
    rabbitmq_handler = None

    def start(self, *args, logger=None, **kwargs):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :param logger:     logging application
        :return: N/A
        """
        self.logger = logger

        rabbitmq_handler = RabbitMQHandler(logger=logger)
        rabbitmq_handler.start()
        self.rabbitmq_handler = rabbitmq_handler

        self.logger.write_to_log(
            LOG_LEVEL_DEBUG, self.application_name, "Started."
        )

    def stop(self):
        """
        Stop lifecycle hook for all applications following the simple
        lifecycle management pattern. This hook should ensure that all resources
        related to this application are released.

        :return: N/A
        """
        self.rabbitmq_handler.stop()

        self.logger.write_to_log(
            LOG_LEVEL_DEBUG, self.application_name, "Stopped."
        )

    def status(self):
        """
        Status information for the application. This function should
        return information about the application's current state.

        :return: N/A
        """
        pass

    def produce_local(self, queue, message):
        """
        Produces a message in the core Python process only. This can be used to
        announce happenings or distribute updates. Topics are not created
        dynamically, but are statically defined in topics.py

        :param queue: states which queue the message should be published to
        :param message: message content to publish
        """
        pass

    def produce_global(self, queue, message):
        """
        As opposed to produce_local, produce_global sends a message on a
        machine global message queue, using RabbitMQ. The message queue does not
        have to be local to the HUME's core process and can be used by any
        program running on the same machine. Topics are not created
        dynamically, but are statically defined in topics.py

        :param queue: states which queue the message should be published to
        :param message: message content to publish
        """
        pass
