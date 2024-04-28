from . import app
from flask import render_template, redirect, url_for, request, flash, request
from flask_login import current_user, login_user,  logout_user, login_required
import sqlalchemy as sql_al
from app import db
from app.models import User
from urllib.parse import urlsplit
# This file is responsible for the routing between the different flask python files and front end html files

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [{
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'},
    {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
    }]
    return render_template('home.html', posts=posts)


# Plain landing page
@app.route('/landing')
def landing():
    return render_template('landing.html')

# Require authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = db.session.scalar(sql_al.select(User).where(User.email == email))
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=True)
        flash('DEBUGGING: USER LOGIN SUCCESSFULLY')
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "POST":
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmed_password = request.form.get('confirm-password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 character.', category='error')
        elif password != confirmed_password:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password is too shor, must be at least 7 character.', category='error')
        else: # everything is correct
            user = User(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!', category='success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return render_template('landing.html')


@app.route('/create_post', methods=['POST'])
@login_required  
def create_post():
    title = request.form['title']
    body = request.form['body']
    if not title or not body:
        flash('Post must have a title and body.')
        return redirect(url_for('index'))

    new_post = Post(title=title, body=body, author=current_user)
    db.session.add(new_post)
    db.session.commit()
    flash('Your post has been created!')
    return redirect(url_for('index'))
