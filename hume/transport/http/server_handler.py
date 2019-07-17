import zmq


def start():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:5556")

    print("Started server handler")

    while True:
        print("Waiting to receive message from HTTP server...")
        msg = socket.recv_json()  # Blocking call
        print(msg)
