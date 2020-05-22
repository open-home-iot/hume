from bottle import request, route, template


@route('/attach')
def attach():
    print(request.json)
    # return template('<b>Hello {{name}}</b>!', id=id)
