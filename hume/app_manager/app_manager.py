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


def initiate():
    app_manager = AppManager()

    # Handle signals
    signal_handling.bind_signal_handlers(app_manager)

    # Parse args
    arg_parser.parse_args(app_manager)

    # Start application
    app_manager.start()

    # While running, provide CLI interface
    cli.start_cli(app_manager)


class AppManager:

    applications = dict()

    def start(self):
        print("Starting applications and services")

        print("Starting utility applications")
        self.start_utility_applications()

        print("Starting transport applications")
        self.start_transport_applications()

        print("Starting business applications")
        self.start_business_applications()

        print("Started all applications")

    def stop(self):
        self.shutdown_gracefully()

    def shutdown_gracefully(self):
        for key, application in self.applications.items():
            print("Stopping %s" % application)
            application.stop()

    def start_utility_applications(self):
        utility_application_modules = [(defs.APPL_UTIL_BROKER, broker),
                                       (defs.APPL_UTIL_LOG, log),
                                       (defs.APPL_UTIL_SCHEDULER, scheduler),
                                       (defs.APPL_UTIL_STORAGE, storage)]

        for key, module in utility_application_modules:
            self.start_application(key, module)

    def start_transport_applications(self):
        transport_application_modules = [(defs.APPL_TRANS_HTTP, http),
                                         (defs.APPL_TRANS_SERIAL, serial)]

        for key, module in transport_application_modules:
            self.start_application(key, module)

    def start_business_applications(self):
        business_application_modules = [(defs.APPL_BUSIN_DEVICE, device),
                                        (defs.APPL_BUSIN_HINT, hint)]

        for key, module in business_application_modules:
            self.start_application(key, module)

    def start_application(self, app_key, module):
        application_instance = module.start()
        print("Started %s" % application_instance)
        self.applications[app_key] = application_instance

    def interrupt(self, signum, frame):
        self.shutdown_gracefully()

        # TODO Do NOT NOT NOT remove this exception raise.
        raise SystemExit("Shutting down application manager")
