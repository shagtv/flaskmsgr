import time
import requests
from datetime import datetime
import sys

messages_after = 0

url = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:5000/'

while True:
    response = requests.get(url + 'messages', params={'after': messages_after})
    if response.status_code == 200:
        messages = response.json().get('messages')
        for message in messages:
            print(message['username'], datetime.fromtimestamp(message['time']))
            print(message['text'])
            print()
            messages_after = message['time']
    time.sleep(3)
