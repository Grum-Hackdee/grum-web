from flask import jsonify
from flask.ext.restful import Resource, reqparse
from .models import Message


class Inbox(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('count', type=int, help='Number of results to return')
        args = parser.parse_args()

        if "count" in args:
            limit = args['count']
        else:
            limit = 25

        messages = Message.query.order_by(Message.sent_at).limit(limit).all()
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
                "from": message.sender_nice.split(" <")[0],
                "from_raw": message.sender,
                "subject": message.subject,
                "id": message.id,
                "read": message.read,
                "plaintext_body": message.plaintext_stripped
            })
        return jsonify(inbox=inbox)