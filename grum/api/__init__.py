from flask import Blueprint
from flask.ext.restful import Api


api = Blueprint("api", __name__, template_folder="templates")
rest = Api(api)

# Import the non-restful resources
from grum.api import mailgun

# Let's get restful!
from grum.api.inbox import Inbox
rest.add_resource(Inbox, '/inbox')

from grum.api.messages import Messages
rest.add_resource(Messages, '/messages/<string:message_id>')

from grum.api.accounts import Account, Accounts
rest.add_resource(Account, '/accounts/<string:address>')
rest.add_resource(Accounts, '/accounts')

from grum.api.user import UserApi
rest.add_resource(UserApi, '/users/<int:userid>')