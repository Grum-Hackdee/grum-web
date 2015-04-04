from flask import Blueprint
from flask.ext.restful import Api


api = Blueprint("api", __name__, template_folder="templates")
rest = Api(api)

from grum.api import models

# Let's get routing!
from grum.api.inbox import Inbox
rest.add_resource(Inbox, '/inbox')