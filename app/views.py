from app import app
from os import path
from flask import send_from_directory, render_template
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
    track = sp.search("In%The%Stone").pop()
    return render_template("home.html", track=track)

@app.route('/logout')
def logout():
    return render_template("unauthenticated.html")
