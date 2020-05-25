import logging

from . import device_timer
from .models import *
from device_controller.util import storage


LOGGER = logging.getLogger(__name__)


def start():
    """
    Starts up the config server.
    """
    LOGGER.info("config start")

    # Register and fetch saved config data, the register action does both ;-)
    storage.register(DeviceActionTimer)

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


def new_configuration(uuid, config):
    """
    Interface for handling configuration changes.

    :param uuid: device ID
    :param config: new configuration
    :return:
    """
    LOGGER.info(f"device: {uuid} new configuration: {config}")

    timers = config["timers"]

    for timer in timers:
        # action path
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

    # schedules = config["schedules"]
    # triggers = config["triggers"]
