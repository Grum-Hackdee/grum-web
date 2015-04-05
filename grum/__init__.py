import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

app = Flask(__name__)
if "DEBUG" in os.environ:
    app.config['DEBUG'] = True
    app.debug=True

if "SENTRY_DSN" in os.environ:
    app.config['SENTRY_DSN'] = os.environ['SENTRY_DSN']

    from raven.contrib.flask import Sentry
    sentry = Sentry(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]

db = SQLAlchemy(app)

from grum.api import api
app.register_blueprint(api, url_prefix='/api')

from grum import views, models
