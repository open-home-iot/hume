import logging

from queue import Queue
from threading import Thread

from device_controller.utility.procedures.procedure import Procedure


LOGGER = logging.getLogger(__name__)

_queue = Queue()
_started = False


def run_in_procedure(caller, *args):
    """
    Puts the called on queue to be called in isolation from other ongoing work.

    :param caller: caller that wants to be queued up
    :param args: arguments that should be supplied with the subsequent call to
                 the caller when the time comes
    """
    assert issubclass(caller.__class__, Procedure)

    global _started
    if not _started:
        _start()
        _started = True

    _queue.put((caller, args))
    LOGGER.debug(f"current number of queued procedures {_queue.qsize()}")


def _monitor_procedure_queue():
    """
    Monitoring procedure queue.
    """
    LOGGER.debug("monitoring procedure queue")
    while True:
        # Blocking
        item = _queue.get()

        (caller, args) = item
        LOGGER.debug(f"procedure starting for {caller}")

        # *args to pack into wanted format again
        caller.start_procedure(*args)


def _start():
    """
    Starts a thread which monitors the procedure queue.
    """
    t = Thread(target=_monitor_procedure_queue, daemon=True)
    t.start()
