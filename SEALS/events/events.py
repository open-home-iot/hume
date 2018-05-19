from abc import ABC, abstractmethod

from threading import Thread, Event

# Event sub causes
OFF = '0'
ON = '1'
ERR = '9'

# Event indexing
PROXIMITY_ALARM = '0'
GET_ALARM_STATE = '1'
SET_ALARM_STATE = '2'


class EventThread(ABC, Thread):
    event = Event()

    @abstractmethod
    def notify(self, reply='busy'):
        pass

    def wait(self, timeout=None):
        return self.event.wait(timeout=timeout)

    def clear(self):
        self.event.clear()
