from flask import Flask
# This python file creates the flask app

app = Flask(__name__)

from app import routes

