from threading import Thread, Event


class StoppingThread(Thread):

    def __init__(self, *args, **kwargs):
        super(StoppingThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()
