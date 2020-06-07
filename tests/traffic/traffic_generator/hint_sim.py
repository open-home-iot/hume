import multiprocessing


class HintSim:
    """
    Encapsulates possible actions that the HINT can take, and takes care of
    proper reporting towards the monitor app through the monitor queue.
    """

    def __init__(self, hc_q: multiprocessing.Queue, mq: multiprocessing.Queue):
        self.hc_q = hc_q
        self.mq = mq

    def confirm_attach(self):
        pass

    def device_timer_configuration_create(self):
        pass

    def device_timer_configuration_delete(self):
        pass

    def device_action(self):
        pass

    def sub_device_action(self):
        pass
