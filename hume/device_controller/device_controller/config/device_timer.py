import pprint
import logging
import threading

from device_controller.config.models import DeviceActionTimer
from device_controller.device import application as device_app
from device_controller.device.models import Device
import hume_storage as storage


LOGGER = logging.getLogger(__name__)

_timers: {str: threading.Timer} = {}


def start(device_action_timer: DeviceActionTimer):
    """
    Sets up a new timer and cleans up any old timers with the same device action
    as the target.

    :param device_action_timer:
    """
    LOGGER.debug(f"starting timer: {device_action_timer}")

    try:
        active_timer = _timers.pop(device_action_timer.action)
        active_timer.cancel()

        LOGGER.debug(f"there was already an old timer, cancelling: "
                     f"{active_timer}")
    except KeyError:
        # This is the case if no timer existed before.
        pass

    new_timer = threading.Timer(float(device_action_timer.interval),
                                timeout,
                                args=(device_action_timer,))
    _timers[device_action_timer.action] = new_timer
    new_timer.start()

    LOGGER.debug(f"new _timers: {pprint.pformat(_timers, indent=2)}")


def stop_all():
    """
    Stop all running timers.
    """
    LOGGER.debug("stopping all device timers")
    for timer in _timers.values():
        timer.cancel()


def stop(timer_ref):
    """
    Stop the timer pointed out by parameter.

    :param timer_ref:
    """
    LOGGER.debug(f"stopping device timer: {timer_ref}")
    _timers.pop(timer_ref).cancel()


def timeout(device_action_timer):
    """
    Restarts the timer that timed out.

    :param device_action_timer:
    :return:
    """
    LOGGER.debug(f"timer timed out: {device_action_timer}")

    timer = threading.Timer(float(device_action_timer.interval),
                            timeout,
                            args=(device_action_timer,))
    _timers.update({device_action_timer.action: timer})

    split = device_action_timer.action.split(',')

    uuid = split[0]
    device = storage.get(Device, uuid)
    LOGGER.debug(f"timer timeout found device: {device}")

    if len(split) == 3:
        device_app.sub_device_action(device, int(split[1]), int(split[2]))
    elif len(split) == 2:
        device_app.device_action(device, int(split[1]))

    timer.start()
