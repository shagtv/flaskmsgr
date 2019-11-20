import time
import requests
from datetime import datetime

messages_after = 0

while True:
    response = requests.get('http://127.0.0.1:5000/messages', params={'after': messages_after})
    if response.status_code == 200:
        messages = response.json().get('messages')
        for message in messages:
            print(message['username'], datetime.fromtimestamp(message['time']))
            print(message['text'])
            print()
            messages_after = message['time']
    time.sleep(1)
