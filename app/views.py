from app import app
from os import path
from flask import send_from_directory, render_template

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/')
def index():
    return render_template("home.html")
