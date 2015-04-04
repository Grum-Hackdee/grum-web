import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]

db = SQLAlchemy(app)

from grum.api import api
app.register_blueprint(api, url_prefix='/api')

from grum import views, models