def capability_response(device, data):
    """
    Called when a device responds to a capability request.

    :param device: Device callee
    :param data: capability data
    :return:
    """
    LOGGER.info("handling capability response")
    # TODO: Store the gotten capabilities in HUME as well, HUME needs to
    #  know some things for validation, but add what's needed WHEN it's
    #  needed.
    capabilities = json.loads(data)
    capabilities["identifier"] = device.uuid

    hint_auth = storage.get(HintAuthentication, None)
    if create_device(
            capabilities, hint_auth.session_id, hint_auth.csrf_token
    ):
        LOGGER.info("device created in HINT successfully")

        # Update the device entry, set correct uuid
        storage.delete(device)  # Clear old address-resolved entry from local
        new_device = Device(uuid=capabilities["uuid"],
                            address=device.address,
                            name=device.name,
                            attached=True)
        storage.save(new_device)

        # Update device address entry to enable bi-directional lookups.
        device_address = storage.get(DeviceAddress, device.address)
        device_address.uuid = capabilities["uuid"]
        storage.save(device_address)

    else:
        LOGGER.error("failed to create device")
        attach_failure(device)


def heartbeat_response(device):
    """
    Called when a device responds to a heartbeat request.

    :param device: Device
    """
    LOGGER.info("handling heartbeat response")

    # ISO 8601
    heartbeat_timestamp = datetime.now().isoformat()

    device_health = storage.get(DeviceHealth, device.uuid)
    if device_health is None:
        device_health = DeviceHealth(device.uuid, heartbeat_timestamp)
    else:
        device_health.heartbeat = heartbeat_timestamp

    storage.save(device_health)


def stateful_action_response(device, data):
    """
    :param device:
    :param data:
    """
    LOGGER.info("handling stateful action response")

    decoded = data.decode("utf-8")

    action_response(device,
                    HintMessage.ACTION_STATEFUL,
                    {"group_id": int(decoded[0]),
                     "state_id": int(decoded[1]),
                     "success": bool(decoded[2])})
