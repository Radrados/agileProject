from flask import Flask
# This python file creates the flask app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'agile-project'  # encrypt the cookies and session data of our 


from app import routes

