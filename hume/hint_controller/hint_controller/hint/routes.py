import logging

from bottle import request, route

from hint_controller.messages.application import hint_message, \
    HINT_MESSAGE_CONFIRM_ATTACH


LOGGER = logging.getLogger(__name__)


@route('/attach/<uuid>')
def confirm_attach(uuid):
    LOGGER.info("got message confirm attach from HINT")

    result = hint_message(HINT_MESSAGE_CONFIRM_ATTACH, request.json)

    return {"result": "ok"}
