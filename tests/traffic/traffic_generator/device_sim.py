import multiprocessing


class DeviceSim:
    """
    Encapsulates possible actions that a device can take, and takes care of
    proper reporting towards the monitor app through the monitor queue.
    """

    def __init__(self, mq: multiprocessing.Queue):
        self.mq = mq

    def attach(self):
        pass

    def device_event(self):
        pass

    def sub_device_event(self):
        pass
