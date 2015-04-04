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