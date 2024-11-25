from app import app, logging as logger
from flask_login import current_user, login_required
from os import path
from flask import send_from_directory, render_template, redirect, request

from .models import *
from .newpost_form import PostForm
from .settings_form import SettingsForm
from .post_repository import get_posts
from .user_repository import get_user_byid, is_following, get_user_byusername

"""
Guards pages that require login by redirecting unauthenticated users to the login page.
"""
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

"""
Main page endpoint. Shows the feed of posts.
"""
@app.route('/', methods=['GET', 'POST'])
def index():
    redir = login_guard()
    if redir is not None: return redir

    form = PostForm()
    
    if request.method == 'GET':
        return render_template("home.html", active="home", user=current_user, form=form, posts=get_posts(current_user.user_id))
    
    form.Handler(current_user)

    return redirect('/')

"""
Profile endpoint. Shows the profile of a given user.
"""
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
    
    form.handler(current_user)
    return redirect('/')

"""
Settings endpoint. Gets / changes the settings of the user.
"""
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
                               user= get_user_byid(current_user.user_id), 
                               settings_form=settings_form)
    
    if form.track_id.data:
        form.handler(current_user)
        return redirect('/')
    
    settings_form.Handler(current_user)
    return redirect('/settings')
    
@app.route('/newuser')
@login_required
def newuser():
    return redirect('/settings')