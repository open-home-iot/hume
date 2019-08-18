import zmq


def start():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:5556")

    while True:
        msg = socket.recv_json()  # Blocking call
        print(msg)  # TODO Kept for testing
