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

        try:
            db.session.add(acc)
            db.session.commit()
        except:
            resp = jsonify(status="Resource Already Exists")
            resp.status_code = 409
            return resp

        return jsonify(status="Success")


class Account(Resource):
    def get(self, address):
        '''Get an individual email account information'''
        account = EmailAccount.query.filter_by(address=address).first_or_404()

        return jsonify(account={
            "address": account.address,
            "owner_id": account.owner_id,
            "mg_api": account.mg_api
        })

    def put(self, address):
        '''Update an email account's information'''
        pass

    def delete(self, address):
        '''Delete an email account's information'''
        pass