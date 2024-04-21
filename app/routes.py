from . import app
from flask import render_template, redirect, url_for, request
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
    return render_template('home.html', user=user, posts=posts)


# Plain landing page
@app.route('/landing')
def landing():
    return render_template('landing.html')

# Require authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Assume email and password are correct --> user logs in
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmed_password = request.form.get('confirm-password')

        if password == confirmed_password:
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    return render_template('landing.html')