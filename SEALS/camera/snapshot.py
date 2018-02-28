from picamera import PiCamera
from datetime import datetime
from threading import Thread


def snapshot():
    tag = datetime.now().strftime("%a %d %m %H:%M:%S")
    camera = PiCamera()
    camera.capture(tag)


def concurrent_snapshot():
    thread = Thread(target=snapshot)
    thread.daemon = True
    thread.start()
