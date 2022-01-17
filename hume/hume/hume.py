from app.device import Device
from app.hint import Hint


class Hume:

    def __init__(self):
        self.device = Device()
        self.hint = Hint()

    def start(self):
        """Starts the HUME."""
        self.device.pre_start()
        self.hint.pre_start()

        self.device.start()
        self.hint.start()

        self.device.post_start()
        self.hint.post_start()

    def stop(self):
        """Stops the HUME."""
        self.device.pre_stop()
        self.hint.pre_stop()

        self.device.stop()
        self.hint.stop()

        self.device.post_stop()
        self.hint.post_stop()
