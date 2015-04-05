import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
if "DEBUG" in os.environ:
    app.config['DEBUG'] = True
    app.debug=True

if "SENTRY_DSN" in os.environ:
    app.config['SENTRY_DSN'] = os.environ['SENTRY_DSN']

    from raven.contrib.flask import Sentry
    sentry = Sentry(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SECRET_KEY'] = os.urandom(64)

db = SQLAlchemy(app)
lm = LoginManager(app)

from grum.api import api
app.register_blueprint(api, url_prefix='/api')

from grum import views, models
from grum.models import User

@lm.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()