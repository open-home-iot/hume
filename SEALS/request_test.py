import requests

r = requests.get('http://localhost:8080/events/alarm')

print(r.status_code)