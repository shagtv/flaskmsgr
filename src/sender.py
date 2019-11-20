import atexit
import requests

while True:
    print('Enter username: ', end='')
    username = input()

    print('Enter password: ', end='')
    password = input()

    response = requests.post('http://127.0.0.1:5000/login',
                             json={'username': username, 'password': password})
    if response.status_code == 200:
        break
    else:
        print('Error: ' + response.json().get('error'))


def exit_handler():
    requests.post('http://127.0.0.1:5000/logout',
                  json={'username': username, 'password': password})


atexit.register(exit_handler)

while True:
    print('Text: ', end='')
    text = input()
    if len(text) == 0:
        continue

    response = requests.post('http://127.0.0.1:5000/send',
                             json={'username': username, 'password': password, 'text': text})
    if response.status_code == 200:
        print('Message sent')
        print()
