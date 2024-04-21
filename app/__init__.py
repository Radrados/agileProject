from flask import Flask
from config import Config
# This python file creates the flask app

app = Flask(__name__)
app.config.from_object(Config)


from app import routes

