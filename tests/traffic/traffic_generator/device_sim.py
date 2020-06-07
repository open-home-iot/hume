import multiprocessing


class DeviceSim:
    """
    Encapsulates possible actions that a device can take, and takes care of
    proper reporting towards the monitor app through the monitor queue.
    """

    def __init__(self, dc_q: multiprocessing.Queue, mq: multiprocessing.Queue):
        self.dc_q = dc_q
        self.mq = mq

    def attach(self, params):
        """
        Send a device attach to the DC.
        """
        self.dc_q.put("attach device")
        self.mq.put("attach device")

    def device_event(self):
        pass

    def sub_device_event(self):
        pass
