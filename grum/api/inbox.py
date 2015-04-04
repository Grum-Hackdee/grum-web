from flask import jsonify
from flask.ext.restful import Resource
from .models import Message


class Inbox(Resource):
    def get(self):
        messages = Message.query.order_by(Message.sent_at).limit(25).all()
        inbox = []
        for message in messages:
            inbox.append({
                "timestamp": message.sent_at,
                "from": message.sender_nice,
                "from_raw": message.sender,
                "subject": message.subject,
                "id": message.id
            })
        return jsonify(inbox=messages)