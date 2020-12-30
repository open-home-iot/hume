import logging

from . import device_timer
from .models import DeviceActionTimer

import hume_storage as storage


LOGGER = logging.getLogger(__name__)


def model_init():
    """
    Initialize models.
    """
    LOGGER.info("model-init")
    storage.register(DeviceActionTimer)


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")


def start():
    """
    Starts up the config server.
    """
    LOGGER.info("config start")

    # TODO get all timers and start them
    LOGGER.debug("getting all timers and starting them.")
    timers = storage.get_all(DeviceActionTimer)

    for timer in timers:
        LOGGER.debug(f"starting timer: {timer}")
        device_timer.start(timer)


def stop():
    """
    Stop all running timers and schedules.
    """
    LOGGER.info("config stop")

    device_timer.stop_all()


# TODO re-do interface, split timer -> action_id, interval and add
# TODO device_id=None as kwarg?
def create_timer_configuration(uuid, timer):
    """
    Interface for handling configuration changes.

    :param uuid: device ID
    :param timer: new device timer
    :return: timer reference
    """
    LOGGER.info(f"device: {uuid} new timer: {timer}")

    device_id = timer.get("device_id")
    # if sub-device
    if device_id:
        action_path = f"{uuid},{device_id},{timer['action_id']}"
    else:
        action_path = f"{uuid},{timer['action_id']}"

    # Check if timer already present for action path
    device_action_timer = storage.get(DeviceActionTimer, action_path)
    LOGGER.debug(f"found timer object: {device_action_timer}")

    if device_action_timer:
        # Update interval if found
        LOGGER.debug("timer matched action path")
        device_action_timer.interval = timer["interval"]
    else:
        # Not found, create a new timer
        device_action_timer = DeviceActionTimer(interval=timer["interval"],
                                                action=action_path)

    storage.save(device_action_timer)

    # set timer
    device_timer.start(device_action_timer)

    return action_path


def delete_timer_configuration(uuid, timer):
    """
    Interface for handling configuration changes.

    :param uuid: device ID
    :param timer: reference to existing timer
    :return: reference to deleted timer/None
    """
    LOGGER.info(f"deleting timer with ref: {timer}")

    timer_ref = storage.get(DeviceActionTimer, timer)

    if timer_ref is not None:
        device_timer.stop(timer_ref.action)
        storage.delete(timer_ref)
        return timer_ref.action
    else:
        LOGGER.debug("timer did not exist, nothing is deleted")

    return timer_ref
