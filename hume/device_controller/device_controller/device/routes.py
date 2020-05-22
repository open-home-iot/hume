from bottle import request, route, template

from device_controller.messages.application import device_message, \
    DEVICE_MESSAGE_ATTACH


@route('/attach')
def attach():
    result = device_message(DEVICE_MESSAGE_ATTACH, request.json)

    return {"result": "ok"}
