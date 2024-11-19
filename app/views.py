from app import app, login_manager, admin, logging as logger
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user, login_user
from os import path
from flask import send_from_directory, render_template, redirect, request, json
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from .signup_form import SignupForm
from .newpost_form import PostForm
from .spotify_client import SpotifyClient
from .post_repository import add_post, get_posts, set_like

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

@app.route('/search', methods=['POST'])
def search():
    search_query = request.json['query']

    if search_query == None or '':
        return "{}"
    
    logger.debug(f"Searching Spotify with query: '{search_query}'")

    sp = SpotifyClient()
    tracks = sp.search(search_query)

    for i in range(len(tracks)):
        tracks[i] = tracks[i].to_dict()

    return json.dumps(tracks)

@app.route('/like', methods=['POST'])
def like():
    set_like(current_user.user_id, request.json['post_id'], request.json['state'])
    return json.dumps({'status': 'OK'})

@app.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect('/login')
    
    form = PostForm()
    
    if request.method == 'GET':
        logger.debug("Getting posts.")
        return render_template("home.html", active="home", user=current_user, form=form, posts=get_posts(current_user.user_id))
    
    if form.validate_on_submit():
        logger.debug("Adding post.")

        add_post(current_user.user_id, track_id=form.track_id.data, description=form.description.data)
    else:
        logger.debug("Form invalid.")

    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignupForm()

    if request.method == "GET":
        return render_template("authform.html", authaction='/login', submitbtn_text='Login', form=form, errormessage="t")
    
    username = str.lower(form.username.data)
    
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, form.password.data):
        return render_template("authform.html", 
                               authaction='/login', 
                               submitbtn_text='Login', 
                               form=form, 
                               errormessage="Incorrect login details. Please try again.")
    
    login_user(user) #todo add remember functionality
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == "GET":
        error_type = request.args.get('error')

        if not error_type:
            error_message = ""
        elif str.find(error_type, "userexists"):
            error_message = 'Username already exists. Please try another.'
            print(f"check: {error_type}")
        elif error_type:
            error_message = 'An unexpected error occurred. Please try again.'

        return render_template("authform.html", authaction="/signup", submitbtn_text="Sign up", form=form, error_message=error_message)

    if form.validate_on_submit():
        username = str.lower(form.username.data)

        user = User.query.filter_by(username=username).first()

        if user:
            return redirect('/signup?error="userexists"')

        created_user = User(username=username, 
                            password=generate_password_hash(form.password.data))
        
        db.session.add(created_user)
        db.session.commit()

        return redirect('/')

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/login')

@login_manager.user_loader
def load_user(user_id):

    logger.debug(f"Attempting to load user with ID: {user_id}")
    return User.query.filter_by(user_id=user_id).first()