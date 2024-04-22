from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# This python file creates the flask app

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)  # db object representing the database
Migrate = Migrate(app, db) # migrate object to represent migration engine



from app import routes

