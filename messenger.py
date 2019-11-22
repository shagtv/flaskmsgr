import sys
from PyQt5 import QtWidgets
from design import Ui_MainWindow
import requests
from datetime import datetime
import time
import threading


url = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:5000/'


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.login)
        self.pushButton.clicked.connect(self.send)

        quit = QtWidgets.QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        threading.Thread(target=self.receive, daemon=True).start()

    def closeEvent(self, event):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        requests.post(url + 'logout',
                      json={'username': username, 'password': password})
        event.accept()

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if len(username) == 0 or len(password) == 0:
            return

        response = requests.post(url + 'login',
                                 json={'username': username, 'password': password})
        if response.status_code == 200:
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.plainTextEdit.setEnabled(True)
            self.pushButton.setEnabled(True)

    def send(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.plainTextEdit.toPlainText()

        if len(username) == 0 or len(password) == 0 or len(text) == 0:
            return

        response = requests.post(url + 'send',
                                 json={'username': username, 'password': password, 'text': text})
        if response.status_code == 200:
            self.plainTextEdit.setPlainText('')

    def receive(self):
        messages_after = 0
        while True:
            response = requests.get(url + 'messages', params={'after': messages_after})
            if response.status_code == 200:
                messages = response.json().get('messages')
                for message in messages:
                    time_str = datetime.fromtimestamp(message['time']).strftime('%Y-%m-%d %H:%M:%S')
                    self.textBrowser.append(message['username'] + ': ' + time_str)
                    self.textBrowser.append(str(message['text']))
                    self.textBrowser.append('')
                    messages_after = message['time']
            time.sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = ExampleApp()
    window.show()
    app.exec_()
