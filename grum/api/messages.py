from grum import db

from flask import jsonify
from flask.ext.restful import Resource
from .models import Message


class Messages(Resource):
    def get(self, message_id):
        msg = Message.query.filter_by(id=message_id).first_or_404()

        msg.read = True
        db.session.add(msg)
        db.session.commit()

        return jsonify(message={
            'id': msg.id,
            'from': msg.sender,
            'from_nice': msg.sender_nice,
            'timestamp': msg.sent_at,
            'subject': msg.subject,
            'html': msg.html,
            'html_stripped': msg.html_stripped,
            'plaintext': msg.plaintext,
            'plaintext_stripped': msg.plaintext_stripped,
            'plaintext_stripped_signature': msg.plaintext_stripped_signature
        })