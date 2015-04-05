import bcrypt
from grum import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    display_name = db.Column(db.String(128))

    def __init__(self, username=None, password=None):
        if username:
            self.username = username
        if password:
            self.set_password(password)

    def set_password(self, plaintext_password):
        self.password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())

    def validate_password(self, plaintext_password):
        hashed = bcrypt.hashpw(plaintext_password.encode('utf-8'), bytes(self.password.encode('utf-8')))
        return hashed == bytes(self.password.encode('utf-8'))


class EmailAccount(db.Model):
    address = db.Column(db.String(128), primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mg_api = db.Column(db.String(64))