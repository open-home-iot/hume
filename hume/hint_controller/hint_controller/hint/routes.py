import logging

from bottle import request, route

from hint_controller.messages.application import incoming_hint_message, \
    HINT_MESSAGE_CONFIRM_ATTACH


LOGGER = logging.getLogger(__name__)


@route('/attach/<uuid>')
def confirm_attach(uuid):
    """
    HINT confirms the attach of a device.

    :param uuid:
    :return:
    """
    LOGGER.info("got message confirm attach from HINT")

    result = incoming_hint_message(HINT_MESSAGE_CONFIRM_ATTACH,
                                   request.json,
                                   uuid)

    return {"result": "ok"}
