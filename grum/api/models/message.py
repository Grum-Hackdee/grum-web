from grum import db


class Message(db.Model):
    id = db.Column(db.String(128), primary_key=True)

    recipient = db.Column(db.String(128))
    recipient_nice = db.Column(db.String(128))

    sender = db.Column(db.String(128))
    sender_nice = db.Column(db.String(128))
    sent_at = db.Column(db.Timestamp)

    html = db.Column(db.Text)
    html_stripped = db.Column(db.Text)

    plaintext = db.Column(db.Text)
    plaintext_stripped = db.Column(db.Text)
    plaintext_stripped_signature = db.Column(db.Text)