from queue import Queue
from threading import Thread

from device_controller.utility.procedures.procedure import Procedure


_queue = Queue()
_started = False


def run_in_procedure(caller, *args):
    assert issubclass(caller.__class__, Procedure)

    global _started
    if not _started:
        _start()
        _started = True

    _queue.put((caller, args))
    print(_queue.qsize())


def _monitor_procedure_queue():
    print("procedure monitoring thread started")
    while True:
        # Blocking
        item = _queue.get()

        (caller, args) = item

        # *args to pack into wanted format again
        caller.start_procedure(*args)


def _start():
    t = Thread(target=_monitor_procedure_queue, daemon=True)
    t.start()
