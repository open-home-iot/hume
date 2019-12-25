import zmq

from django.shortcuts import HttpResponse


context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:5556")


def index(request):
    msg = {
        "message_type": 1,
        "content": "hello"
    }
    socket.send_json(msg)

    return HttpResponse("OK!")
