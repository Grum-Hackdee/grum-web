from flask import jsonify
from flask.ext.restful import Resource
from .models import Message


class Inbox(Resource):
    def get(self):
        messages = Message.query.order_by(Message.sent_at).limit(25).all()
        inbox = []
        for message in messages:
            cropped = message.plaintext_stripped

            if "\r\n" in cropped:
                cropped = cropped.split("\r\n")[0]

            if len(cropped) > 120:
                cropped = cropped[117]

            cropped = cropped + "..."

            inbox.append({
                "timestamp": message.sent_at,
                "from": message.sender_nice,
                "from_raw": message.sender,
                "subject": message.subject,
                "id": message.id,
                "read": message.read,
                "plaintext_body": message.plaintext_stripped
            })
        return jsonify(inbox=inbox)