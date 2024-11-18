from app import db
from flask_login import UserMixin

"""
Used to store spotify track IDs for posts.
"""
class Track(db.Model):
    track_id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(50), index=True, unique=True)

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(200))
    bio = db.Column(db.String(1000))
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    likes = db.relationship('Like', backref='user', lazy='dynamic')

    followers = db.relationship('Follow', 
                                foreign_keys='Follow.followed', 
                                backref='follower_list',
                                lazy='dynamic')
    
    following = db.relationship('Follow',
                                foreign_keys='Follow.follower',
                                backref='following_list')

class Follow(db.Model):
    follow_id = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    followed = db.Column(db.Integer, db.ForeignKey('user.user_id'))

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    track_id = db.Column(db.Integer, db.ForeignKey('track.track_id'))
    likes = db.relationship('Like', backref='post', lazy='dynamic')

class Like(db.Model):
    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), index=True)