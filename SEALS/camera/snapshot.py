from picamera import PiCamera
from datetime import datetime
from threading import Thread


hardcoded_pic_dir = '/home/pi/Pictures/'
pic_type = '.jpg'


def snapshot():
    tag = hardcoded_pic_dir + datetime.now().strftime("%a %d %m %H:%M:%S") + pic_type
    camera = PiCamera()
    camera.capture(tag)
    camera.close()


def concurrent_snapshot():
    thread = Thread(target=snapshot)
    thread.daemon = True
    thread.start()
