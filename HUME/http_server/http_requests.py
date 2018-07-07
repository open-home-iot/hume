import requests
import time

from requests.exceptions import ConnectionError


BASE_URL = 'http://localhost:8000/'


def notify_alarm(alarm_status, timestamp):
    alarm_url = 'on/' + timestamp if alarm_status else 'off'
    try:
        print('HTTP REQUESTS: Notifying web server')
        requests.get(BASE_URL + 'events/alarm/' + alarm_url + '/')
    except ConnectionError:
        print('HTTP REQUESTS: Could not notify HTTP server of event, unreachable')


def get_config():
    while 1:
        try:
            result = requests.get(BASE_URL + 'api/surveillance_configuration/1/')
            return result.json()
        except ConnectionError:
            print('HTTP REQUESTS: Could not fetch configuration, destination unreachable')
            time.sleep(5)


