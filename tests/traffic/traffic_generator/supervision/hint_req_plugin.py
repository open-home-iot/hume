import logging
import multiprocessing


LOGGER = logging.getLogger(__name__)

mq: multiprocessing.Queue


"""
When a call is received in this module, the HC supervising process must report
to KPI monitoring to update success/failure ratios and other pertinent info.

Example scenario:
1. HTT triggers a device attach for a device by instructing the DC supervisor to
   trigger a device attach.
2. DC receives a call to its device request handler module and after internal
   handling, forwards the request to HC over RMQ.
3. HC receives the RMQ message and after internal handling forwards it to HINT
   through the HINT request module. Overridden by HTT, this module receives a
   call to the attach function in the space of the HC supervising process.
4. Here, information about the attach request can be forwarded to the monitoring
   system which will confirm that the HTT triggered attach was handled 
   successfully.
"""


def attach(message_content):
    """
    Sends HINT an attach message.

    :param message_content:
    :return:
    """
    print("sending HINT an attach message")
    mq.put("send HINT an attach")


def device_event(message_content):
    """
    Sends HINT an event message.

    :param message_content:
    :return:
    """
    mq.put("send HINT device event")


def sub_device_event(message_content):
    """
    Sends HINT an event message.

    :param message_content:
    :return:
    """
    mq.put("send HINT sub device event")
