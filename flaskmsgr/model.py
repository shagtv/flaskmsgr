from flaskmsgr import  db


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
