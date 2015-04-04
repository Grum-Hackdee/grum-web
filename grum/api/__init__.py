from flask import Blueprint
from flask.ext.restful import Api


api = Blueprint("api", __name__, template_folder="templates")
rest = Api(api)