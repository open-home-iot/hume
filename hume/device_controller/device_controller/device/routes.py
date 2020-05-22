from bottle import request, route, template

from device_controller.messages.application import device_message


@route('/attach')
def attach():
    device_message(request.json)

    return {"result": "ok"}
