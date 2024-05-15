from app import login, app
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sql_al
import sqlalchemy.orm as sql_orm
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id: sql_orm.Mapped[int] = sql_orm.mapped_column(primary_key=True)
    username: sql_orm.Mapped[str] = sql_orm.mapped_column(sql_al.String(64), index=True, unique=True)
    first_name: sql_orm.Mapped[str] = sql_orm.mapped_column(sql_al.String(32), index=True)
    last_name: sql_orm.Mapped[str] = sql_orm.mapped_column(sql_al.String(32), index=True)
    email: sql_orm.Mapped[str] = sql_orm.mapped_column(sql_al.String(120), index=True, unique=True)
    password_hash: sql_orm.Mapped[Optional[str]] = sql_orm.mapped_column(sql_al.String(256))
    posts: sql_orm.WriteOnlyMapped['Post'] = sql_orm.relationship(back_populates='author')
    about_me: sql_orm.Mapped[Optional[str]] = sql_orm.mapped_column(sql_al.String(140))

    # prints object of this class --> debuging 
    def __repr__(self):
        return '<User {}>'.format(self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
# This is temporary the schema will change in the future features
# Need to add:  
    #upvotes, will need to be linked to the user's total number of upvotes
    #comments that are linked to the post in question 
class Post(db.Model):
    id: sql_orm.Mapped[int] = sql_orm.mapped_column(primary_key=True)
    title: sql_orm.Mapped[str] = sql_orm.mapped_column(sql_al.String(32))
    body: sql_orm.Mapped[str] = sql_orm.mapped_column(sql_al.String(140))
    timestamp: sql_orm.Mapped[datetime] = sql_orm.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id: sql_orm.Mapped[int] = sql_orm.mapped_column(sql_al.ForeignKey(User.id), index=True)
    author: sql_orm.Mapped[User] = sql_orm.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)

#table for comments
class Comment(db.Model):
    id: sql_orm.Mapped[int] = sql_orm.mapped_column(primary_key=True)
    body: sql_orm.Mapped[str] = sql_orm.mapped_column(sql_al.String(1000)) #we'll have to decide how long the comments need to be
    timestamp: sql_orm.Mapped[datetime] = sql_orm.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    post_id: sql_orm.Mapped[int] = sql_orm.mapped_column(sql_al.ForeignKey('post.id'), index=True)
    user_id: sql_orm.Mapped[int] = sql_orm.mapped_column(sql_al.ForeignKey('user.id'), index=True)
    author: sql_orm.Mapped[User] = sql_orm.relationship('User', back_populates='comments')
    post: sql_orm.Mapped[Post] = sql_orm.relationship('Post', back_populates='comments')

    def __repr__(self):
        return '<Comment {}>'.format(self.body)

#establishing relationships for the user, post and comment tables
    #stuff like user owns thier posts and comments 
User.comments = sql_orm.relationship('Comment', back_populates='author', foreign_keys=[Comment.user_id]) #each comment to user
Post.comments = sql_orm.relationship('Comment', back_populates='post', foreign_keys=[Comment.post_id], order_by='Comment.timestamp') #implement upvotes, but I reckon it's just adding valudes and letting users increment them
#comment to post

#temporary line to create the tables if there is no existing database
with app.app_context():
    db.create_all()

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
