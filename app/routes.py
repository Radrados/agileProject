from . import app
from flask import render_template
# This file is responsible for the routing between the different flask python files and front end html files

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Radin'}
    return render_template('home.html', title='Home', user=user)