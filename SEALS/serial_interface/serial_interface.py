from queue import Queue
from select import select
from serial import Serial
from threading import Thread, Event


WRITABLE = True

COMMAND_BUFFER = Queue()

CONNECTION = Serial(port='/dev/tty.usbmodem1411', baudrate=9600)


class EventThread(Thread):
    def __init__(self, *args, **kwargs):
        super(EventThread, self).__init__(*args, **kwargs)
        self.event = Event()

    def run(self):
        print("Command waiter started")
        while True:
            self.event.wait()

            command = COMMAND_BUFFER.get()
            print("COMMAND FROM HTTP SERVER")
            print(command)


writer_thread = EventThread()


def start():
    writer_thread.start()
    listener_daemon = Thread(target=serial_select, daemon=True)
    listener_daemon.start()


def serial_select():
    print("Select waiter started")
    while True:
        # Since no timeout is specified, block until read is available
        # ------------------------------
        # BLOCKS
        select([CONNECTION], [], [])
        # ------------------------------
        
        event = CONNECTION.readline()
        event_notification(decode(event))


def decode(message):
    print("Decoding: ", message)
    decoded_string = message.decode('utf-8')
    return decoded_string.strip()


def encode(message):
    print("Encoding: ", message)
    return message.encode('utf-8')


def event_notification(event=None):
    print("EVENT FROM ARDUINO!")
    print(event)


def execute_command(command=None):
    COMMAND_BUFFER.put(command)
    writer_thread.event.set()


if __name__ == '__main__':
    start()
