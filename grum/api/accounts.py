import requests

from grum import db
from grum.models import User, EmailAccount
from flask import jsonify, request
from flask.ext.restful import Resource

MAILGUN_API_BASE = "https://api.mailgun.net/v3/"
MAILGUN_API_ENDPOINT = "/messages"

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

        return jsonify(status="Success", account=acc)


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
        # Here be dragons
        account = EmailAccount.query.filter_by(address=address).first_or_404()
        try:
            db.session.delete(account)
            db.session.commit()
        except:
            resp = jsonify(status="Error")
            resp.status_code = 500
            return resp
        return jsonify(status="Success")

    def post(self, address):
        '''We POST to send mail'''
        account = EmailAccount.query.filter_by(address=address).first_or_404()
        owner = User.query.filter_by(id=account.owner_id).first()

        mail = request.get_json()

        domain = address.split("@")[1]
        mg_url = MAILGUN_API_BASE + domain + MAILGUN_API_ENDPOINT

        res = requests.post(
            mg_url,
            auth=("api", account.mg_api),
            data={
                "from": owner.get_formatted_from(address),
                "to": str(mail['to']),
                "subject": str(mail['subject']),
                "text": str(mail['text'])
            }
        )

        if res.status_code == 200:
            return jsonify(status="Success!")