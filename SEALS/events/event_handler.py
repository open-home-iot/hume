from threading import Thread, Event


class EventThread(Thread):
    event = Event()

    def wait(self, timeout=None):
        return self.event.wait(timeout=timeout)

    def clear(self):
        self.event.clear()
