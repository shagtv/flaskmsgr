from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/status')
def status():
    return {
        'status': True
    }


@app.route('/date')
def date():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


if __name__ == '__main__':
    app.run()
