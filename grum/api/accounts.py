from grum import db
from grum.models import User, EmailAccount
from flask import jsonify, request
from flask.ext.restful import Resource


class Accounts(Resource):
    def get(self):
        accounts = EmailAccount.query.all()

        output = []
        for account in accounts:
            output.append({
                "address": account.address,
                "owner_id": account.owner_id
            })

        return jsonify(accounts=output)

    def post(self):
        '''Create a new email account'''
        inc = request.get_json()

        user = User.query.filter_by(id=int(inc['owner_id'])).first_or_404()
        acc = EmailAccount(
            address=str(inc['address']),
            owner_id=user.id,
            mg_api=str(inc['mg_api'])
        )

        db.session.add(acc)
        db.session.commit()

        return jsonify(status="Success")


class Account(Resource):
    def get(self, account_id):
        '''Get an individual email account information'''
        pass

    def put(self, account_id):
        '''Update an email account's information'''
        pass

    def delete(self, account_id):
        '''Delete an email account's information'''
        pass