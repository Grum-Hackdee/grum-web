from grum import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    to = db.Column(db.String(64))
    cc = db.Column(db.String(64))

    subject = db.Column(db.String(256))
    body = db.Column(db.Text)