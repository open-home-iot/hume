from transport import http
from transport import serial
from utility import broker
from utility import log
from utility import scheduler
from utility import storage
from business import device
from business import hint

from . import signal_handling
from . import cli
from . import arg_parser
from . import defs
from .application_abc import ApplicationABC


def initiate():
    # Parse args
    arg_parser.parse_args()

    app_manager = AppManager()

    # Handle signals
    signal_handling.bind_signal_handlers(app_manager)

    # Start application
    app_manager.start()

    # While running, provide CLI
    cli.start_cli(app_manager)


class AppManager(ApplicationABC):

    applications = dict()

    def start(self):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.

        :return: N/A
        """

        print("Starting applications")

        print("Starting utility applications")
        self.start_utility_applications()

        print("Starting transport applications")
        self.start_transport_applications()

        print("Starting business applications")
        self.start_business_applications()

        print("Started all applications")

    def stop(self):
        """
        Stop lifecycle hook for all applications following the simple
        lifecycle management pattern. This hook should ensure that all resources
        related to the Application Manager is released and that every sub-
        application is also stopped so that they in turn can release resources
        and shut down.

        :return: N/A
        """

        for key, application in self.applications.items():
            print("Stopping %s" % application)
            application.stop()

    def status(self):
        """
        Status information for the application manager. This function should
        return information about the application manager's current state.

        :return: N/A
        """

        pass

    def start_utility_applications(self):
        """
        Starts all utility related applications of the HUME system. Utility
        applications are defined under .../hume/utility.

        :return: N/A
        """

        utility_application_modules = [(defs.APPL_UTIL_LOG, log),
                                       (defs.APPL_UTIL_BROKER, broker),
                                       (defs.APPL_UTIL_SCHEDULER, scheduler),
                                       (defs.APPL_UTIL_STORAGE, storage)]

        for key, module in utility_application_modules:
            self.start_utility_application(key, module)

    def start_utility_application(self, app_key, module):
        """
        Start a single utility application and register it with the application
        manager's register of applications.

        :param app_key: identifier for the application about to be started, used
                        for instant access to its instance in the application
                        registry.
        :param module:  module containing the application that is about to be
                        started.
        :return:        N/A
        """

        application_instance = module.start()

        print("Started %s" % application_instance)
        self.applications[app_key] = application_instance

    def start_transport_applications(self):
        """
        Starts all transport related applications of the HUME system. Transport
        applications are defined under .../hume/transport.

        :return: N/A
        """

        transport_application_modules = [(defs.APPL_TRANS_HTTP, http),
                                         (defs.APPL_TRANS_SERIAL, serial)]

        utility_applications = [
            self.applications[defs.APPL_UTIL_LOG],
            self.applications[defs.APPL_UTIL_BROKER],
            self.applications[defs.APPL_UTIL_STORAGE],
            self.applications[defs.APPL_UTIL_SCHEDULER]
        ]

        for key, module in transport_application_modules:
            self.start_transport_application(
                key,
                module,
                utility_applications=utility_applications
            )

    def start_transport_application(self,
                                    app_key,
                                    module,
                                    utility_applications=None):
        """
        Start a single transport application and register it with the
        application manager's register of applications.

        :param app_key: identifier for the application about to be started, used
                        for instant access to its instance in the application
                        registry.
        :param module:  module containing the application that is about to be
                        started.
        :param utility_applications: a list of all utility applications that the
                                     transport application is allowed to use.
        :return:        N/A
        """

        application_instance = module.start(
            utility_applications=utility_applications
        )

        print("Started %s" % application_instance)
        self.applications[app_key] = application_instance

    def start_business_applications(self):
        """
        Starts all business related applications of the HUME system. Transport
        applications are defined under .../hume/business.

        :return: N/A
        """

        business_application_modules = [(defs.APPL_BUSIN_DEVICE, device),
                                        (defs.APPL_BUSIN_HINT, hint)]

        utility_applications = [
            self.applications[defs.APPL_UTIL_LOG],
            self.applications[defs.APPL_UTIL_BROKER],
            self.applications[defs.APPL_UTIL_STORAGE],
            self.applications[defs.APPL_UTIL_SCHEDULER]
        ]

        transport_applications = [
            self.applications[defs.APPL_TRANS_HTTP],
            self.applications[defs.APPL_TRANS_SERIAL]
        ]

        for key, module in business_application_modules:
            self.start_business_application(
                key,
                module,
                utility_applications=utility_applications,
                transport_applications=transport_applications
            )

    def start_business_application(self,
                          app_key,
                          module,
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
        :param utility_applications:   a list of all utility applications that
                                       the business application is allowed to
                                       use.
        :param transport_applications: a list of all transport applications that
                                       the business application is allowed to
                                       use.
        :return:        N/A
        """

        application_instance = module.start(
            utility_applications=utility_applications,
            transport_applications=transport_applications
        )

        print("Started %s" % application_instance)
        self.applications[app_key] = application_instance

    def interrupt(self, signum, frame):
        """
        Used to handle the SIGINT signal, so that the HUME system can be shut
        down gracefully, even after an interrupt.

        :param signum: <see python docs>
        :param frame:  <see python docs>
        :return:       N/A
        """

        self.stop()

        # TODO Do NOT NOT NOT remove this exception raise.
        raise SystemExit("Shutting down application manager")
