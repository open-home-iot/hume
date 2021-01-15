import threading
import time
import requests
import json
import random

from bottle import run, get, response

from device_controller.device.http_server import MyServer


"""
This module implements a simple device simulator. It consists of a small web
service which listens for capability, heartbeat, and action requests and
replies to them as a normal device would. The device simulator simulates only
one device, a thermometer. Upon starting the simulator, an attach request will
be sent to HUME.
"""


server = MyServer(host='localhost', port=32222)
server_thread: threading.Thread

ACTION_TEMPERATURE = "0"
ACTION_HUMIDITY = "1"


def start_simulator():
    """
    Starts the device simulator web server.
    """

    def run_server():
        """
        Target of the server thread.
        """
        run(server=server)

    global server_thread
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    # Wait a bit before attaching to let HUME start
    time.sleep(2)
    requests.post("http://localhost:8081/devices/attach",
                  json={"uuid": "86e467d9-02b4-4119-940d-a871750aa997"})


def stop_simulator():
    """
    Stops the device simulator.
    """
    server.shutdown()
    server_thread.join()


@get('/capabilities')
def capabilties():
    """
    When HUME requests the device to send its capabilities through a
    capability request.

    :returns: bottle.response
    """
    response.status = 200
    response.body = json.dumps(
        {
            "uuid": "e2bf93b6-9b5d-4944-a863-611b6b6600e7",
            "name": "THERMO X2",
            "description": "Combined Thermometer and Humidity sensor.",
            "category": 0,
            "type": 0,
            "data_types": {
                "0": "Temperature",
                "1": "Humidity"
            },
            "actions": [
                {
                    "id": 0,
                    "name": "Read temperature",
                    "type": 1,
                    "data_type": "0",
                    "return_type": 2

                },
                {
                    "id": 1,
                    "name": "Read humidity",
                    "type": 1,
                    "data_type": "1",
                    "return_type": 2
                }
            ]
        }
    )

    return response


@get('/heartbeat')
def heartbeat():
    """
    When HUME requests to see if the device is still alive.
    """
    # No need to fill in anything, an empty response = 200
    pass


@get('/actions/<action_id>')
def action(action_id):
    """
    HUME wants to execute a device action.

    :param action_id: points out which action to execute
    :return: bottle.response
    """
    # both actions return a float, but humidity is a range between 0.0 and
    # 100.0 while temperature is assumed to be indoor and between 19.0 and
    # 30.0 degrees celsius.
    if action_id == ACTION_TEMPERATURE:
        val = random.uniform(19.0, 30.0)
    elif action_id == ACTION_HUMIDITY:
        val = random.uniform(0.0, 100.0)

    response.body = json.dumps({"value": f"{val:.2f}"})

    return response
