from .. import ApplicationABC


class DeviceApplication(ApplicationABC):

    def start(self, utility_applications=None, transport_applications=None):
        pass

    def stop(self):
        pass

    def status(self):
        pass
