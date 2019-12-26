from multiprocessing import Process

from lib.application_base import ApplicationABC
from operations.log.application import Logger, LOG_LEVEL_DEBUG
from utility.broker.rabbitmq_handler.AsyncConsumer import AsyncConsumer
from utility.broker.topics import *


class RabbitMQHandler(ApplicationABC):

    application_name = 'RabbitMQHandler'

    _consumer_process = None

    logger: Logger = None

    def __init__(self, logger=None):
        """
        Constructor for the RabbitMQHandler.

        :param logger: logging application
        """
        self.logger = logger

    def start(self):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :return: N/A
        """
        async_consumer = AsyncConsumer(logger=self.logger, queues=GLOBAL_TOPICS)
        self._consumer_process = Process(target=async_consumer.run)
        self._consumer_process.start()

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
        self._consumer_process.terminate()
        self._consumer_process.join()

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
