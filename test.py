#from flask import Flask
# This is a basic flask app, provided in week 6 lecture "Flask Server Side Rendering"
# To run: flask run

# Create flask object: stores everything about webserver and operates it
#app = Flask(__name__)

# RESPONSE TO A CLIENT REQUEST
# The app object is given a decorator: meta information to the function
# Calls the function at the top level url of the website
#@app.route("/")
#def hello():
#    return "Hello World!"

# if the app name is called then run app, prevents accidentally running the app.
#if __name__== "__main__":
#    app.run()