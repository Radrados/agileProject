from . import app
from flask import render_template
# This file is responsible for the routing between the different flask python files and front end html files

@app.route('/')
@app.route('/index')
def index():
    # reference: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates
    # this is only to have something in the webserver to see when webpage is rendered
    user = {'username': 'Radin'}
    posts = [{
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'},
    {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
    }]
    return render_template('home.html', title='Home', user=user, posts=posts)


# Plain landing page
@app.route('/landing')
def landing():
    return render_template('landing.html')

# Require authentication
@app.route('/login')
def login():
    return render_template('login.html', title='Login')

@app.route('/register')
def register():
    return render_template('register.html', title='Register')

@app.route('/logout')
def logout():
    return render_template('landing.html')