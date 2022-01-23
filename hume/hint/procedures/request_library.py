def broker_credentials(session_id):
    """
    Requests broker credentials from HINT.

    :param session_id: session ID to authenticate the request
    :returns: broker credentials
    :rtype: dict | None
    """
    LOGGER.info("requesting broker credentials")

    response = requests.get(_hint_api_url() + "humes/broker-credentials",
                            cookies={"sessionid": session_id})

    print(response.cookies)

    if response.status_code == requests.codes.ok:
        return response.json()


def create_device(capabilities: dict,
                  session_id: str,
                  csrf_token: str) -> bool:
    """
    Sends a create device request to HINT with the provided capabilities.

    :param capabilities: HOME-compliant capabilities, to be encoded as JSON
    :param session_id: session ID to authenticate the request
    :param csrf_token: CSRF token
    :return: True if successful
    """
    LOGGER.info("sending create device request")

    response = requests.post(
        f"{_hint_api_url()}humes/{get_arg(CLI_HUME_UUID)}/devices",
        json=capabilities,
        cookies={"sessionid": session_id,
                 "csrftoken": csrf_token},
        headers={"X-CSRFToken": csrf_token})

    print(response.cookies)

    if response.status_code == requests.codes.created:
        return True
    return False
