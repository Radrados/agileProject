from . import app
from flask import render_template, redirect, url_for, request, flash, request
from flask_login import current_user, login_user,  logout_user, login_required
import sqlalchemy as sql_al
from app import db
from app.models import User, Post, Comment, Tag
from urllib.parse import urlsplit

# This file is responsible for the routing between the different flask python files and front end html files
# This is the route to the home page
@app.route('/')
@app.route('/index')
##@login_required
def index():
    page = request.args.get('page', 1, type=int)
    #displays all the posts in home page
    query = Post.query.order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=app.config['POST_PER_PAGE'], error_out=False)
    next_url, prev_url = None, None
    if posts.has_next:
        next_url = url_for('index', page=posts.next_num)
    if posts.has_prev:
        prev_url = url_for('index', page=posts.prev_num)
    return render_template('home.html', posts=posts.items, next_url=next_url, prev_url=prev_url)


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
            flash('Invalid username or password', category='danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=True)
        flash('You have successfully logged in', category='success')
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

        email_exist = User.query.filter_by(email=email).first()
        user_exist = User.query.filter_by(username=username).first()
        if email_exist:
            flash('Email already exists.', category='danger')
        elif user_exist:
            flash('Username already exists.', category='danger')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='danger')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 character.', category='danger')
        elif password != confirmed_password:
            flash('Passwords don\'t match.', category='danger')
        elif len(password) < 8:
            flash('Password is too short, must be at least 8 character.', category='danger')
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
@app.route('/create_post', methods=['GET', 'POST'])  # Allow both GET and POST methods
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']  # Retrieve data from the HTML form
        body = request.form['body']
        comment_body = request.form.get('comment')
        tags = request.form.get('tags')

        if not title or not body:
            flash('Post must have a title and body.', category='danger')
            return render_template('create_post.html')  # Stay on the same page to show errors

        new_post = Post(title=title, body=body, author=current_user)
        db.session.add(new_post)
        db.session.commit()

        if tags:
            tag_names = [name.strip() for name in tags.split(',')]
            for name in tag_names:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag(name=name)
                    db.session.add(tag)
                new_post.tags.append(tag)
            db.session.commit()

        if comment_body:  # If the comment field is filled, create the comment
            comment = Comment(body=comment_body, post_id=new_post.id, user_id=current_user.id)
            db.session.add(comment)
            db.session.commit()

        flash('Your post has been created!', category='success')
        return redirect(url_for('index'))
    else:  # This block is for handling GET requests
        return render_template('create_post.html')

@app.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    #query = tag.posts.order_by(Post.timestamp.desc())
    query = Post.query.filter(Post.tags.any(id=tag.id)).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=app.config['POST_PER_PAGE'], error_out=False)
    next_url, prev_url, = None, None
    if posts.has_next:
        next_url = url_for('tag', tag_name=tag_name, page=posts.next_num)
    if posts.has_prev:
        prev_url = url_for('tag', tag_name=tag_name, page=posts.prev_num)
    return render_template('tag.html', tag=tag, posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id) #get the post, 404 if can't be found
    comments = Comment.query.filter_by(post_id=post_id, parent_id=None).order_by(Comment.timestamp.asc()).all() #all orphan comments
    
    if request.method == 'POST': #
        comment_body = request.form.get('comment')
        parent_id = request.form.get('parent_id', type=int)  # Optional parent comment id
        if comment_body:
            comment = Comment(body=comment_body, post_id=post_id, user_id=current_user.id, parent_id=parent_id)
            db.session.add(comment)
            db.session.commit()
            flash('Comment added', category='success')
            return redirect(url_for('post', post_id=post_id))
    
    return render_template('post.html', post=post, comments=comments)


# Route to user profile page
@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sql_al.select(User).where(User.username == username))
    page = request.args.get('page', 1, type=int)
    query = user.posts.select().order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=app.config['POST_PER_PAGE'], error_out=False)
    next_url, prev_url = None, None
    if posts.has_next:
        next_url = url_for('user', username=user.username, page=posts.next_num)
    if posts.has_prev:
        prev_url = url_for('user', username=user.username, page=posts.prev_num)
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/search', methods=['POST'])
def search(): 
    search_post = request.form.get('search-post')
    if not search_post:
        flash('You must enter textphrase to search for in title', category='danger')
        return redirect(url_for('index'))
    
    # If the user searchs for i.e. 'Introductory Chugg' but there is only 'Introductory to Chugg', we will not get the result
    # Split the search_post string into an array of tags and query for each tag
    search_tags = search_post.split(' ')
    if not search_tags:
        flash("No valid tags found", category='danger')
        return redirect(url_for('index'))
    
    conditions = [] # creating a list of search conditions
    for tag in search_tags: # for each tag in the array, search the Post title and body for the tag
        conditions.append(Post.title.ilike(f'%{tag}%'))
        conditions.append(Post.body.ilike(f'%{tag}%'))
        
    query = sql_al.or_(*conditions) # create the query that will accept the tags either in the title or the body
    search_results = Post.query.filter(query).order_by(Post.timestamp.desc()).all()      
    return render_template('home.html', posts=search_results)


@app.route('/upvote/<int:post_id>', methods=['POST'])
@login_required
def upvote(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user not in post.upvoted_by:
        post.upvoted_by.append(current_user)
        post.upvotes += 1
        db.session.commit()
        flash('Post upvoted!', category='success')
    else:
        flash('You have already upvoted this post.', category='danger')
    return redirect(url_for('post', post_id=post_id))

@app.route('/unupvote/<int:post_id>', methods=['POST'])
@login_required
def unupvote(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user in post.upvoted_by:
        post.upvoted_by.remove(current_user)
        post.upvotes -= 1
        db.session.commit()
        flash('Post un-upvoted.', category='success')
    else:
        flash('You have not upvoted this post.', category='danger')
    return redirect(url_for('post', post_id=post_id))
