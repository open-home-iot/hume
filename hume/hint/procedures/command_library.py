def attach_failure(device):
    """
    Indicates to HINT a failure to attach the input device.

    :param device: Device
    """
    LOGGER.info("sending attach failure to HINT")

    message = {
        "type": HintMessage.ATTACH_DEVICE,
        "content": {
            "identifier": device.uuid,
            "success": False,
        },
    }

    publish(message)


def action_response(device, action_type, info: dict):
    """
    Indicates to HINT the response to an action request.

    :param device:
    :param action_type:
    :param info: information about the action
    """
    LOGGER.info("sending action response to HINT")

    message = {
        "type": action_type,
        "device_uuid": device.uuid,
        "content": info
    }

    publish(message)
