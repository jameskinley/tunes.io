from app import app, login_manager, admin, logging as logger
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user, login_user, login_required
from os import path
from flask import send_from_directory, render_template, redirect, request, json
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from .signup_form import SignupForm
from .newpost_form import PostForm, post_form_handler
from .settings_form import SettingsForm
from .spotify_client import SpotifyClient
from .post_repository import get_posts, set_like
from .user_repository import *

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Follow, db.session))
admin.add_view(ModelView(Like, db.session))

def login_guard():
    if not current_user.is_authenticated:
        logger.info("User is not authenticated. Redirecting to login.")
        return redirect('/login')
    
def inverse_login_guard():
    if current_user.is_authenticated:
        logger.info("User is already authenticated. Loading home page.")
        return redirect('/')

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
    
    post_form_handler(form, current_user)

    return redirect('/')

@app.route('/follow', methods=['POST'])
@login_required
def follow():
    if set_follow(current_user.user_id, request.json['username'], request.json['state']):
        return json.dumps({'status': 'OK'})
    return json.dumps({'status': 'ERROR'})

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    redir = login_guard()
    if redir is not None: return redir

    form = PostForm()

    if request.method == 'GET':
        username = request.args.get('user')
        if username == '' or username == None:
            return redirect('/')
        
        user = get_user_byusername(username)

        if user is None:
            return redirect('/')
        
        is_current_user = False
        following = False

        if user.user_id == current_user.user_id:
            is_current_user = True
        else:
            following = is_following(current_user.user_id, user.user_id)

        return render_template("profile.html", 
                               posts=get_posts(current_user.user_id, user.user_id), 
                               form=form, 
                               user=user, 
                               is_current_user=is_current_user,
                               following=following)
    
    post_form_handler(form, current_user)
    return redirect('/')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    redir = login_guard()
    if redir is not None: return redir

    form = PostForm(prefix='post')
    settings_form = SettingsForm(prefix='settings')

    if request.method == 'GET':
        settings_form.SetUserDefaults(current_user)
        return render_template("settings.html", 
                               form=form, 
                               user= load_user(current_user.user_id), 
                               settings_form=settings_form)
    
    if form.track_id.data:
        post_form_handler(form, current_user)
        return redirect('/')
    
    settings_form.Handler(current_user)
    return redirect('/settings')

@app.route('/login', methods=['GET', 'POST'])
def login():
    redir = inverse_login_guard()
    if redir is not None: return redir

    form = SignupForm()

    if request.method == "GET":
        return render_template("authform.html", authaction='/login', submitbtn_text='Login', form=form)
    
    username = str.lower(form.username.data)
    
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, form.password.data):
        # Say incorrect login details regardless of whether account exists. This prevents bad actors from working out account names as easily.
        return render_template("authform.html", 
                               authaction='/login', 
                               submitbtn_text='Login', 
                               form=form, 
                               error_message="Incorrect login details. Please try again.")
    
    login_user(user, form.remember.data)
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    redir = inverse_login_guard()
    if redir is not None: return redir

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
        
        if form.confirm_password.data != form.password.data:
            return redirect('/signup?error="no"')

        created_user = User(username=username, 
                            password=generate_password_hash(form.password.data))
        
        db.session.add(created_user)
        db.session.commit()

        login_user(user)
        return redirect('/newuser')
    
    return render_template("authform.html", authaction="/signup", submitbtn_text="Sign up", form=form, error_message="Unable to create account. Please try again.")
    
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