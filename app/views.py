from app import app, login_manager, admin, logging as logger
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user, login_user, login_required
from os import path
from flask import send_from_directory, render_template, redirect, request, json
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from .signup_form import SignupForm
from .newpost_form import PostForm, post_form_handler
from .spotify_client import SpotifyClient
from .post_repository import get_posts, set_like
from .user_repository import get_user_byid, get_user_byusername

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Follow, db.session))
admin.add_view(ModelView(Like, db.session))

def login_guard():
    if not current_user.is_authenticated:
        logger.info("User is not authenticated. Redirecting to login.")
        return redirect('/login')

"""
Serves the favicon request. 
Code adapted from https://flask.palletsprojects.com/en/stable/patterns/favicon/
"""
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/search', methods=['POST'])
@login_required
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
@login_required
def like():
    set_like(current_user.user_id, request.json['post_id'], request.json['state'])
    return json.dumps({'status': 'OK'})

@app.route('/', methods=['GET', 'POST'])
def index():
    redir = login_guard()
    if redir is not None: return redir

    form = PostForm()
    
    if request.method == 'GET':
        return render_template("home.html", active="home", user=current_user, form=form, posts=get_posts(current_user.user_id))
    
    post_form_handler(form)

    return redirect('/')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    redir = login_guard()
    if redir is not None: return redir

    form = PostForm()

    if request.method == 'GET':
        username = request.args.get('user')
        if username is '' or username is None:
            return redirect('/')
        
        user = get_user_byusername(username)

        if user is None:
            return redirect('/')
        
        is_current_user = False
        if user.user_id == current_user.user_id:
            is_current_user = True

        return render_template("profile.html", 
                               posts=get_posts(current_user.user_id, user.user_id), 
                               form=form, 
                               user=user, 
                               is_current_user=is_current_user)
    
    post_form_handler()
    return redirect('/')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    redir = login_guard()
    if redir is not None: return redir
    form = PostForm()

    if request.method == 'GET':
        return render_template("settings.html", form=form, user= load_user(current_user.user_id))
    
    post_form_handler()
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

        login_user(user)
        return redirect('/newuser')
    
@app.route('/newuser')
@login_required
def newuser():
    return redirect('/settings')

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/login')

@login_manager.user_loader
def load_user(user_id):
    logger.debug(f"Attempting to load user with ID: {user_id}")
    return get_user_byid(user_id)