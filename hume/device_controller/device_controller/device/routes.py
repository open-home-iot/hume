from bottle import route, template


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)
