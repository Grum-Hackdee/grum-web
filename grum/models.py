import bcrypt
from grum import db
from flask.ext.login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    display_name = db.Column(db.String(128))

    def __init__(self, username=None, display_name=None, password=None):
        if username:
            self.username = username
        if display_name:
            self.display_name = display_name
        if password:
            self.set_password(password)

    def get_display_name(self):
        if self.display_name:
            return self.display_name
        else:
            return self.username

    def set_password(self, plaintext_password):
        self.password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())

    def validate_password(self, plaintext_password):
        hashed = bcrypt.hashpw(plaintext_password.encode('utf-8'), bytes(self.password.encode('utf-8')))
        return hashed == bytes(self.password.encode('utf-8'))

    def get_formatted_from(self, address):
        output = ""

        if self.display_name:
            output = self.display_name + " "
        else:
            output = self.username + " "

        output += "<" + address + ">"
        return output


class EmailAccount(db.Model):
    address = db.Column(db.String(128), primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mg_api = db.Column(db.String(64))