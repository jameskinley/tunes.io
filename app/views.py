from app import app, login_manager, admin
from flask_admin.contrib.sqla import ModelView
from os import path
from flask import send_from_directory, render_template
from .models import *
from .spotify_client import SpotifyClient

admin.add_view(ModelView(Track, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Follow, db.session))
admin.add_view(ModelView(Like, db.session))

"""
Serves the favicon request. 
Code adapted from https://flask.palletsprojects.com/en/stable/patterns/favicon/
"""
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/')
def index():
    sp = SpotifyClient()
    track = sp.search("yellow coldplay")[0]
    return render_template("home.html", track=track)

@app.route('/login')
def login():
    return 'Login'

@app.route('/register')
def register():
    return 'Register'

@app.route('/logout')
def logout():
    return render_template("unauthenticated.html")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)