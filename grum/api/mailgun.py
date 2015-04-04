from grum import db
from grum.api import api
from grum.api.models import Message
from flask import request, Response


@api.route("/mailgun", methods=["POST"])
def receive_from_mailgun():
    d = request.form
    newmail = Message(
        id=d['Message-Id'],
        recipient=d['recipient'],
        recipient_nice=d['To'],
        sender=d['sender'],
        sender_nice=d['from'],
        sent_at=d['timestamp'],
        subject=d['subject'],
        html=d['body-html'],
        html_stripped=d['stripped-html'],
        plaintext=d['body-plain'],
        plaintext_stripped=d['stripped-text'],
        plaintext_stripped_signature=d['stripped-signature'],
        read=False
    )

    db.session.add(newmail)
    db.session.commit()

    return Response(status=200)