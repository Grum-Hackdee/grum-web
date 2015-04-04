from flask import jsonify
from flask.ext.restful import Resource


class Inbox(Resource):
    def get(self):
        return jsonify(inbox=[])