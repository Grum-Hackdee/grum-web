from grum.models import User, EmailAccount
from flask import jsonify
from flask.ext.restful import Resource


class UserApi(Resource):
    def get(self, userid):
        user = User.query.filter_by(id=userid).first_or_404()
        email_accounts = EmailAccount.query.filter_by(owner_id=user.id).all()
        addresses = []

        for email in email_accounts:
            addresses.append(email.address)

        return jsonify(user={
            'username': user.username,
            'id': user.id,
            'display_name': user.get_display_name(),
            'emails': addresses
        })