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
    print("confirming attach from plugin module")
    mq.put((device, "confirming attach"))


def device_action(device, action_id):
    """
    Sends a device an action invocation.

    :param device:
    :param action_id:
    :return:
    """
    mq.put((device, "device action"))


def sub_device_action(device, device_id, action_id):
    """
    Sends a sub device an action invocation.

    :param device:
    :param device_id:
    :param action_id:
    :return:
    """
    mq.put((device, "sub device action"))
