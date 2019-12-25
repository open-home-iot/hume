from transport.http_listener.application import HttpListener
from transport.http_communicator.application import HttpCommunicator
from transport.serial_listener.application import SerialListener
from transport.serial_communicator.application import SerialCommunicator

from utility.broker.application import Broker
from operations.log.application import Logger, \
    LOG_LEVEL_INFO, LOG_LEVEL_WARNING
from utility.scheduler.application import Scheduler
from utility.storage.application import Storage

from business.device.application import Device
from business.hint.application import Hint

from . import signal_handling
from . import cli
from . import arg_parser
from lib.application_base import ApplicationABC


def initiate():
    # Parse args
    cli_args = arg_parser.parse_args()

    app_manager = AppManager()

    # Handle signals
    signal_handling.bind_signal_handlers(app_manager)

    # Start application
    app_manager.start(cli_args=cli_args)

    # While running, provide CLI
    cli.start_cli(app_manager)


class AppManager(ApplicationABC):

    application_name = 'AppManager'

    logger: Logger = None  # Typed for ease-of-access.

    applications = dict()

    # ------------------------------------------
    # APPLICATION MODULE REGISTRATION LISTS
    # ------------------------------------------

    # BASIC LAYER
    operations_applications = [
        Logger
    ]

    # UTILITY LAYER, STARTS FIRST
    utility_applications = [
        Broker,
        Storage,
        Scheduler
    ]

    # TRANSPORT LAYER, STARTS SECOND
    transport_applications = [
        HttpCommunicator,
        HttpListener,
        SerialCommunicator,
        SerialListener
    ]

    # BUSINESS LAYER, STARTS THIRD
    business_applications = [
        Device,
        Hint
    ]

    def start(self, *args, cli_args=None, **kwargs):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :param cli_args: arguments passed at the start of this program, which
                         can be relayed to a specific application or kept in the
                         application manager.
        :return:         N/A
        """

        self.configure_operations(cli_args=cli_args)

        # No need to check if cli_args is None since the object always exists
        # after parsing arguments, even if there were no arguments.
        self.start_utility_applications(cli_args=cli_args)
        self.logger.write_to_log(
            LOG_LEVEL_INFO,
            self.application_name,
            "Started utility applications."
        )

        self.start_transport_applications(cli_args=cli_args)
        self.logger.write_to_log(
            LOG_LEVEL_INFO,
            self.application_name,
            "Started transport applications."
        )

        self.start_business_applications(cli_args=cli_args)
        self.logger.write_to_log(
            LOG_LEVEL_INFO,
            self.application_name,
            "Started business applications."
        )

    def stop(self):
        """
        Stop lifecycle hook for all applications following the simple
        lifecycle management pattern. This hook should ensure that all resources
        related to the Application Manager is released and that every sub-
        application is also stopped so that they in turn can release resources
        and shut down.

        :return: N/A
        """
        self.logger.write_to_log(
            LOG_LEVEL_INFO,
            self.application_name,
            "Stopping system."
        )

        for key, application in self.applications.items():
            self.logger.write_to_log(
                LOG_LEVEL_INFO,
                self.application_name,
                "Stopping {}.".format(application.application_name)
            )
            application.stop()

        self.logger.write_to_log(
            LOG_LEVEL_INFO,
            self.application_name,
            "Stopped all running applications, exiting now."
        )

    def status(self):
        """
        Status information for the application manager. This function should
        return information about the application manager's current state.

        :return: status integer
        """

        pass

    def configure_operations(self, cli_args=None):
        for application in self.operations_applications:
            application_instance = application()
            application_instance.start(cli_args=cli_args)
            self.applications[application.application_name] = application_instance

        self.logger = self.applications[Logger.application_name]

    def start_utility_applications(self, cli_args=None):
        """
        Starts all utility related applications of the HUME system. Utility
        applications are defined under .../hume/utility.

        :param cli_args: arguments intended for a utility application.
        :return: N/A
        """
        for application in self.utility_applications:
            self.start_utility_application(application, cli_args=cli_args)

    def start_utility_application(self, application, cli_args=None):
        """
        Start a single utility application and register it with the application
        manager's register of applications.

        :param application: Python class to instantiate
        :param cli_args: arguments intended for a utility application.
        :return:        N/A
        """
        self.logger.write_to_log(
            LOG_LEVEL_INFO,
            self.application_name,
            "Starting {}.".format(application.application_name)
        )

        application_instance = application()
        application_instance.start(
            cli_args=cli_args,
            logger=self.applications[Logger.application_name]
        )
        self.applications[application.application_name] = application_instance

    def start_transport_applications(self, cli_args=None):
        """
        Starts all transport related applications of the HUME system. Transport
        applications are defined under .../hume/transport.

        :param cli_args: arguments intended for a transport application.
        :return: N/A
        """
        for application in self.transport_applications:
            self.start_transport_application(application, cli_args=cli_args)

    def start_transport_application(self, application, cli_args=None):
        """
        Start a single transport application and register it with the
        application manager's register of applications.

        :param application: Python class to instantiate
        :param cli_args:    arguments intended for a transport application.
        :return:        N/A
        """

        application_instance = application()
        application_instance.start(
            cli_args=cli_args,
            logger=self.applications[Logger.application_name],
            scheduler=self.applications[Scheduler.application_name],
            broker=self.applications[Broker.application_name],
            storage=self.applications[Storage.application_name]
        )
        self.applications[application.application_name] = application_instance

    def start_business_applications(self, cli_args=None):
        """
        Starts all business related applications of the HUME system. Transport
        applications are defined under .../hume/business.

        :param cli_args: arguments intended for a business application.
        :return: N/A
        """
        for application in self.business_applications:
            self.start_business_application(application, cli_args=cli_args)

    def start_business_application(self, application, cli_args=None):
        """
        Start a single business application and register it with the
        application manager's register of applications.

        :param application: Python class to instantiate
        :param cli_args:    arguments intended for a business application.
        :return:        N/A
        """
        application_instance = application()
        application_instance.start(
            cli_args=cli_args,
            logger=self.applications[Logger.application_name],
            scheduler=self.applications[Scheduler.application_name],
            broker=self.applications[Broker.application_name],
            storage=self.applications[Storage.application_name],
            http_communicator=self.applications[HttpCommunicator.application_name],
            serial_communicator=self.applications[SerialCommunicator.application_name]
        )
        self.applications[application.application_name] = application_instance

    def interrupt(self, signum, frame):
        """
        Used to handle the SIGINT signal, so that the HUME system can be shut
        down gracefully, even after an interrupt.

        :param signum: <see python docs>
        :param frame:  <see python docs>
        :return:       N/A
        """
        self.logger.write_to_log(
            LOG_LEVEL_WARNING,
            self.application_name,
            "SIGINT was received, stopping system."
        )

        self.stop()

        # TODO Do NOT NOT NOT remove this exception raise.
        raise SystemExit("Shutting down application manager")
