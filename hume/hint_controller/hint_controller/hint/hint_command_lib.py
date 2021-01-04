import logging
import json

from rabbitmq_client.client import RMQClient

from hint_controller.util.args import get_arg, HUME_UUID


LOGGER = logging.getLogger(__name__)

HINT_MASTER_COMMAND_QUEUE = "hint_master"


class HintClient:
    client: RMQClient

    @staticmethod
    def command(command):
        """
        :type command: dict
        """
        command["uuid"] = get_arg(HUME_UUID)

        encoded_command = json.dumps(command).encode('utf-8')

        HintClient.client.command(HINT_MASTER_COMMAND_QUEUE,
                                  encoded_command)


def init(client):
    """
    :type client: RMQClient
    """
    HintClient.client = client


def discover_devices_done(command):
    """
    This is just a forward of what was returned by DC since the messages look
    exactly the same.

    :type command: dict
    """
    LOGGER.info("sending discover devices result back to HINT")
    LOGGER.debug(f"discovery result: {command}")
    HintClient.command(command)
