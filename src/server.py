from flask import Flask, request
from datetime import datetime
import time

app = Flask(__name__)

messages = []
users = {}
users_online = set()


@app.route('/status')
def status():
    return {
        'users': len(users),
        'users_online': len(users_online),
        'messages': len(messages),
    }


@app.route('/date')
def date():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')

    if len(username) == 0 or len(password) == 0:
        return {'error': 'Empty username or password'}, 401

    if len(password) < 5:
        return {'error': 'Password must have at least 5 chars'}, 401

    if username not in users or users[username] == password:
        users[username] = password
        users_online.add(username)
        messages.append({'username': 'bot', 'text': username + ' logged in', 'time': time.time()})
        return {'ok': True}
    else:
        return {'error': 'Invalid username or password'}, 401


@app.route('/logout', methods=['POST'])
def logout():
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    if username in users_online and users[username] == password:
        users_online.remove(username)
        messages.append({'username': 'bot', 'text': username + ' logged out', 'time': time.time()})
    return {'ok': True}


@app.route('/send', methods=['POST'])
def send():
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    text = request.json.get('text', '')

    if len(text) == 0:
        return {'ok': False}, 403

    if username not in users or users[username] != password:
        return {'ok': False}, 401

    messages.append({'username': username, 'text': text, 'time': time.time()})

    if text == '/status':
        messages.append({'username': 'bot', 'text': status(), 'time': time.time()})
    elif text == '/date':
        messages.append({'username': 'bot', 'text': date(), 'time': time.time()})

    return {'ok': True}


@app.route('/messages')
def messages_method():
    after = float(request.args.get('after', 0))
    filtered_messages = [message for message in messages if message['time'] > after]
    return {'messages': filtered_messages}


if __name__ == '__main__':
    app.run(debug=True)
