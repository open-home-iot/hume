from transport import http_listener
from transport import http_communicator
from transport import serial_listener
from transport import serial_communicator

from utility import broker
from utility import log
from utility.log.application import LogApplication, \
    LOG_LEVEL_INFO, LOG_LEVEL_WARNING
from utility import scheduler
from utility import storage

from business import device
from business import hint

from . import signal_handling
from . import cli
from . import arg_parser
from . import defs
from lib.application_base import ApplicationABC


def initiate():
    # Parse args
    args = arg_parser.parse_args()

    app_manager = AppManager()

    # Handle signals
    signal_handling.bind_signal_handlers(app_manager)

    # Start application
    app_manager.start(args=args)

    # While running, provide CLI
    cli.start_cli(app_manager)


class AppManager(ApplicationABC):

    application_name = 'AppManager'

    log_application: LogApplication = None  # Typed for ease-of-access.

    applications = dict()

    def start(self, args=None):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :param args: arguments passed at the start of this program, which can
                     be relayed to a specific application or kept in the
                     application manager.
        :return:     N/A
        """

        # No need to check if args is None since the object always exists after
        # parsing arguments, even if there were no arguments.
        self.start_utility_applications(args=args)

        self.log_application = self.applications[defs.APPL_UTIL_LOG]
        self.log_application.write_to_log(
            LOG_LEVEL_INFO,
            self.application_name,
            "Started utility applications."
        )

        self.start_transport_applications(args=args)
        self.log_application.write_to_log(
            LOG_LEVEL_INFO,
            self.application_name,
            "Started transport applications."
        )

        self.start_business_applications(args=args)
        self.log_application.write_to_log(
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
        self.log_application.write_to_log(
            LOG_LEVEL_INFO,
            self.application_name,
            "Stopping system."
        )

        for key, application in self.applications.items():
            application.stop()

        self.log_application.write_to_log(
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

    def start_utility_applications(self, args=None):
        """
        Starts all utility related applications of the HUME system. Utility
        applications are defined under .../hume/utility.

        :param args: arguments intended for a utility application.
        :return: N/A
        """

        utility_application_modules = [(defs.APPL_UTIL_LOG, log),
                                       (defs.APPL_UTIL_BROKER, broker),
                                       (defs.APPL_UTIL_SCHEDULER, scheduler),
                                       (defs.APPL_UTIL_STORAGE, storage)]

        for key, module in utility_application_modules:
            self.start_utility_application(key, module, args=args)

    def start_utility_application(self, app_key, module, args=None):
        """
        Start a single utility application and register it with the application
        manager's register of applications.

        :param app_key: identifier for the application about to be started, used
                        for instant access to its instance in the application
                        registry.
        :param module:  module containing the application that is about to be
                        started.
        :param args:    arguments intended for a utility application.
        :return:        N/A
        """

        application_instance = module.start(args=args)
        self.applications[app_key] = application_instance

    def start_transport_applications(self, args=None):
        """
        Starts all transport related applications of the HUME system. Transport
        applications are defined under .../hume/transport.

        :param args: arguments intended for a transport application.
        :return: N/A
        """

        transport_application_modules = [(defs.APPL_TRANS_HTTP_LISTENER,
                                          http_listener),
                                         (defs.APPL_TRANS_HTTP_COMMUNICATOR,
                                          http_communicator),
                                         (defs.APPL_TRANS_SERIAL_LISTENER,
                                          serial_listener),
                                         (defs.APPL_TRANS_SERIAL_COMMUNICATOR,
                                          serial_communicator)]

        utility_applications = {
            defs.APPL_UTIL_LOG:
                self.applications[defs.APPL_UTIL_LOG],
            defs.APPL_UTIL_BROKER:
                self.applications[defs.APPL_UTIL_BROKER],
            defs.APPL_UTIL_STORAGE:
                self.applications[defs.APPL_UTIL_STORAGE],
            defs.APPL_UTIL_SCHEDULER:
                self.applications[defs.APPL_UTIL_SCHEDULER]
        }

        for key, module in transport_application_modules:
            self.start_transport_application(
                key,
                module,
                args=args,
                utility_applications=utility_applications
            )

    def start_transport_application(self,
                                    app_key,
                                    module,
                                    args=None,
                                    utility_applications=None):
        """
        Start a single transport application and register it with the
        application manager's register of applications.

        :param app_key: identifier for the application about to be started, used
                        for instant access to its instance in the application
                        registry.
        :param module:  module containing the application that is about to be
                        started.
        :param args:    arguments intended for a transport application.
        :param utility_applications: a dict of all utility applications that the
                                     transport application is allowed to use.
        :return:        N/A
        """

        if utility_applications is None:
            utility_applications = []

        application_instance = module.start(
            args=args,
            utility_applications=utility_applications
        )

        self.applications[app_key] = application_instance

    def start_business_applications(self, args=None):
        """
        Starts all business related applications of the HUME system. Transport
        applications are defined under .../hume/business.

        :param args: arguments intended for a business application.
        :return: N/A
        """

        business_application_modules = [(defs.APPL_BUSIN_DEVICE, device),
                                        (defs.APPL_BUSIN_HINT, hint)]

        utility_applications = {
            defs.APPL_UTIL_LOG:
                self.applications[defs.APPL_UTIL_LOG],
            defs.APPL_UTIL_BROKER:
                self.applications[defs.APPL_UTIL_BROKER],
            defs.APPL_UTIL_STORAGE:
                self.applications[defs.APPL_UTIL_STORAGE],
            defs.APPL_UTIL_SCHEDULER:
                self.applications[defs.APPL_UTIL_SCHEDULER]
        }

        transport_applications = {
            defs.APPL_TRANS_HTTP_COMMUNICATOR:
                self.applications[defs.APPL_TRANS_HTTP_COMMUNICATOR],
            defs.APPL_TRANS_HTTP_LISTENER:
                self.applications[defs.APPL_TRANS_HTTP_LISTENER],
            defs.APPL_TRANS_SERIAL_COMMUNICATOR:
                self.applications[defs.APPL_TRANS_SERIAL_COMMUNICATOR],
            defs.APPL_TRANS_SERIAL_LISTENER:
                self.applications[defs.APPL_TRANS_SERIAL_LISTENER]
        }

        for key, module in business_application_modules:
            self.start_business_application(
                key,
                module,
                args=args,
                utility_applications=utility_applications,
                transport_applications=transport_applications
            )

    def start_business_application(self,
                                   app_key,
                                   module,
                                   args=None,
                                   utility_applications=None,
                                   transport_applications=None):
        """
        Start a single business application and register it with the
        application manager's register of applications.

        :param app_key: identifier for the application about to be started, used
                        for instant access to its instance in the application
                        registry.
        :param module:  module containing the application that is about to be
                        started.
        :param args:    arguments intended for a business application.
        :param utility_applications:   a dict of all utility applications that
                                       the business application is allowed to
                                       use.
        :param transport_applications: a dict of all transport applications that
                                       the business application is allowed to
                                       use.
        :return:        N/A
        """

        if transport_applications is None:
            transport_applications = []
        if utility_applications is None:
            utility_applications = []

        application_instance = module.start(
            args=args,
            utility_applications=utility_applications,
            transport_applications=transport_applications
        )

        self.applications[app_key] = application_instance

    def interrupt(self, signum, frame):
        """
        Used to handle the SIGINT signal, so that the HUME system can be shut
        down gracefully, even after an interrupt.

        :param signum: <see python docs>
        :param frame:  <see python docs>
        :return:       N/A
        """
        self.log_application.write_to_log(
            LOG_LEVEL_WARNING,
            self.application_name,
            "SIGINT was received, stopping system."
        )

        self.stop()

        # TODO Do NOT NOT NOT remove this exception raise.
        raise SystemExit("Shutting down application manager")
