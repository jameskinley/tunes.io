from app import app, login_manager
from os import path
from flask import send_from_directory, render_template, Blueprint
from .spotify_client import SpotifyClient

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
    track = sp.search("In%The%Stone")[0]
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
