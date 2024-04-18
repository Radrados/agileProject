from app import app
# This file is responsible for the routing between the different flask python files and front end html files

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"