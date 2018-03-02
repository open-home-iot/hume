from picamera import PiCamera
from datetime import datetime
from threading import Thread
from .picture_storage import get_picture_directory


def snapshot():
    tag = get_picture_directory() + datetime.now().strftime("%a %d %m %H:%M:%S") + '.jpg'
    camera = PiCamera()
    camera.capture(tag)
    camera.close()


def concurrent_snapshot():
    thread = Thread(target=snapshot)
    thread.daemon = True
    thread.start()
