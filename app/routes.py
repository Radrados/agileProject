from . import app
from flask import render_template, redirect, url_for, request, flash, request
from flask_login import current_user, login_user,  logout_user, login_required
import sqlalchemy as sql_al
from app import db
from app.models import User, Post, Comment
from urllib.parse import urlsplit

# This file is responsible for the routing between the different flask python files and front end html files
# This is the route to the home page
@app.route('/')
@app.route('/index')
##@login_required
def index():
    #displays all the posts in home page
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('home.html', posts=posts)


# Route to landing/introductory page for instructions on app services
@app.route('/landing')
def landing():
    return render_template('landing.html')

# Route to login page
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

# Register route to create new accounts
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

#add posts and comments to the database
@app.route('/create_post', methods=['POST']) # the route accessing which creates a post
@login_required  
def create_post(): #post creation
    title = request.form['title'] #retrieve data from the html form
    body = request.form['body']
    comment_body = request.form.get('comment')

    if not title or not body:
        flash('Post must have a title and body.')
        #the flashes don't show up anywhere rn, but they're useful to have
        return redirect(url_for('index'))

    new_post = Post(title=title, body=body, author=current_user)
    db.session.add(new_post)
    db.session.commit()

    if comment_body: # if the comment field is filled in makes the comment
        comment = Comment(body=comment_body, post_id=new_post.id, user_id=current_user.id)
        db.session.add(comment)
    db.session.commit()
    flash('Your post has been created!')
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.desc()).all()
    if request.method == 'POST':
        comment_body = request.form.get('comment')
        if comment_body:
            comment = Comment(body=comment_body, post_id=post_id, user_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added.', category='success')
            return redirect(url_for('post', post_id=post_id))
    return render_template('post.html', post=post, comments=comments)


# Route to user profile page
@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sql_al.select(User).where(User.username == username))
    posts = Post.query.filter_by(user_id = user.id)
    posts = posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)

@app.route('/search', methods=['POST'])
def search(): 
    search_post = request.form.get('search-post')
    if not search_post:
        flash('You must enter textphrase to search for in title', category='error')
        return redirect(url_for('index'))
    
    # If the user searchs for i.e. 'Introductory Chugg' but there is only 'Introductory to Chugg', we will not get the result
    # Split the search_post string into an array of tags and query for each tag
    search_tags = search_post.split(' ')
    if not search_tags:
        flash("No valid tags found", category='error')
        return redirect(url_for('index'))
    
    conditions = [] # creating a list of search conditions
    for tag in search_tags: # for each tag in the array, search the Post title and body for the tag
        conditions.append(Post.title.ilike(f'%{tag}%'))
        conditions.append(Post.body.ilike(f'%{tag}%'))
        
    query = sql_al.or_(*conditions) # create the query that will accept the tags either in the title or the body
    search_results = Post.query.filter(query).all()       
    return render_template('home.html', posts=search_results)