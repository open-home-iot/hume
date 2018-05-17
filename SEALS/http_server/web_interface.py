import requests

from requests import exceptions as request_exceptions


def notify_alarm(alarm_url):
    try:
        requests.get('http://localhost:8000/api/events/alarm/' + alarm_url)
    except request_exceptions.ConnectionError:
        print('WEB INTERFACE: Could not notify HTTP server of event, unreachable')
