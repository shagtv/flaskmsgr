import atexit
import requests
import sys

url = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:5000/'

while True:
    print('Enter username: ', end='')
    username = input()

    print('Enter password: ', end='')
    password = input()

    response = requests.post(url + 'login',
                             json={'username': username, 'password': password})
    if response.status_code == 200:
        break
    else:
        print('Error: ' + response.json().get('error'))


def exit_handler():
    requests.post(url + 'logout',
                  json={'username': username, 'password': password})


atexit.register(exit_handler)

while True:
    print('Text: ', end='')
    text = input()
    if len(text) == 0:
        continue

    response = requests.post(url + 'send',
                             json={'username': username, 'password': password, 'text': text})
    if response.status_code == 200:
        print('Message sent')
        print()
