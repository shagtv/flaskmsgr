from flask import render_template, request
from flaskmsgr.model import Messages, Users
from datetime import datetime
from flaskmsgr import application, db
import time


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/status')
def status():
    return {
        'users': Users.query.count(),
        'users_online': Users.query.filter_by(online=True).count(),
        'messages': Messages.query.count(),
    }


@application.route('/date')
def date():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


@application.route('/clear_messages')
def clear_messages():
    deleted = Messages.query.delete()
    db.session.commit()
    return {'ok':  deleted}


@application.route('/clear_users')
def clear_users():
    deleted = Users.query.delete()
    db.session.commit()
    return {'ok': deleted}


@application.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')

    if len(username) == 0 or len(password) == 0:
        return {'error': 'Empty username or password'}, 401

    if len(password) < 5:
        return {'error': 'Password must have at least 5 chars'}, 401

    user = Users.query.filter_by(username=username).first()
    correct = False
    if user is None:
        correct = True
        new_user = Users(username=username, password=password, online=True)
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            print('Error')
    elif user.password == password:
        correct = True
        user.online = True
        db.session.commit()

    if correct:
        save_message('bot', username + ' logged in')
        return {'ok': True}
    else:
        return {'error': 'Invalid username or password'}, 401


@application.route('/logout', methods=['POST'])
def logout():
    username = request.json.get('username', '')
    password = request.json.get('password', '')

    user = Users.query.filter_by(username=username).first()
    if user is not None and user.password == password:
        user.online = False
        db.session.commit()
        save_message('bot', username + ' logged out')
    return {'ok': True}


@application.route('/send', methods=['POST'])
def send():
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    text = request.json.get('text', '')

    if len(text) == 0:
        return {'ok': False}, 403

    user = Users.query.filter_by(username=username).first()
    if user is None or user.password != password:
        return {'ok': False}, 401

    save_message(username, text)

    if text == '/status':
        save_message('bot', str(status()))
    elif text == '/date':
        save_message('bot', date())

    return {'ok': True}


def save_message(username, text):
    new_message = Messages(username=username, text=text, time=time.time())
    try:
        db.session.add(new_message)
        db.session.commit()
    except:
        print('Error')


@application.route('/messages')
def messages_method():
    after = float(request.args.get('after', 0))
    filtered_messages = Messages.query.filter(Messages.time > after).order_by(Messages.time).all()
    return {'messages': [i.serialize for i in filtered_messages]}


@application.route('/users')
def users():
    online_users = Users.query.filter_by(online=True).all()
    return {'users': [i.username for i in online_users]}
