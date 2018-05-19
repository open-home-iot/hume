import requests

from requests.exceptions import ConnectionError


def notify_alarm(alarm_status, timestamp):
    alarm_url = 'on/' if alarm_status else 'off/'
    try:
        requests.get('http://localhost:8000/api/events/alarm/' + alarm_url + timestamp)
    except ConnectionError:
        print('HTTP REQUESTS: Could not notify HTTP server of event, unreachable')


