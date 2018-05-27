import requests

res = requests.get('http://localhost:8080/get_alarm_state')
print(res.text)
print(res.content)
