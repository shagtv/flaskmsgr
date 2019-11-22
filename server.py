from flask import Flask, request, render_template
from datetime import datetime
import time
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    text = db.Column(db.String(255))
    time = db.Column(db.Float)

    def __repr__(self):
        return self.username + ':' + self.text

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'username': self.username,
            'text': self.text,
            'time': self.time
        }


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    online = db.Column(db.Boolean)

    def __repr__(self):
        return self.username


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

    all_messages = Messages.query.order_by(Messages.time).all()

    filtered_messages = [message for message in all_messages if message.time > after]
    return {'messages': [i.serialize for i in filtered_messages]}


@application.route('/users')
def users():
    online_users = Users.query.filter_by(online=True).all()
    return {'users': [i.username for i in online_users]}


if __name__ == '__main__':
    application.run(debug=True)
