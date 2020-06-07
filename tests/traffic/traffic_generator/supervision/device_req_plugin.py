import logging
import multiprocessing


LOGGER = logging.getLogger(__name__)

mq: multiprocessing.Queue


"""
When a call is received in this module, the DC supervising process must report
to KPI monitoring to update success/failure ratios and other pertinent info.
"""


def confirm_attach(device):
    """
    Sends the parameter device an attach confirm message

    :param device:
    :return:
    """
    LOGGER.debug(f"sending confirm attach request to device: {device.uuid}")


def device_action(device, action_id):
    """
    Sends a device an action invocation.

    :param device:
    :param action_id:
    :return:
    """
    LOGGER.debug(f"sending device action: {device} {action_id}")


def sub_device_action(device, device_id, action_id):
    """
    Sends a sub device an action invocation.

    :param device:
    :param device_id:
    :param action_id:
    :return:
    """
    LOGGER.debug(f"sending sub device action: {device} {device_id} {action_id}")
