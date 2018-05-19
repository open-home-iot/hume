from picamera import PiCamera
from threading import Thread
from .picture_storage import get_picture_directory


def snapshot(timestamp):
    tag = get_picture_directory() + timestamp + '.jpg'
    camera = PiCamera()
    camera.capture(tag)
    camera.close()


def concurrent_snapshot(timestamp):
    thread = Thread(target=snapshot, args=timestamp)
    thread.daemon = True
    thread.start()
