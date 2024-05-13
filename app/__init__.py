from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
# This python file creates the flask app

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)  # db object representing the database
migrate = Migrate(app, db)  # migrate object to represent migration engine
login = LoginManager(app)
login.login_view = 'login'
moment = Moment(app)

from app import routes, models

