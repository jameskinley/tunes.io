from app import app, login_manager, admin
from flask_admin.contrib.sqla import ModelView
from os import path
from flask import send_from_directory, render_template, redirect
from .models import *
from .signup_form import SignupForm
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
    return render_template("home.html", track=track, active="home")

@app.route('/profile')
def profile():
    return render_template("profile.html", active="profile")

@app.route('/login')
def login():
    return render_template("authform.html", authaction='/login', submitbtn_text='Login', form=SignupForm())

@app.route('/signup')
def signup():
    return render_template("authform.html", authaction="/signup", submitbtn_text="Sign up", form=SignupForm())

@app.route('/logout')
def logout():
    return redirect('/login')

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)