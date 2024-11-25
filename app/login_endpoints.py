from app import app, db, login_manager, logging as logger
from .signup_form import SignupForm
from flask_login import current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, request, render_template
from .models import User
from .user_repository import get_user_byid
    
def inverse_login_guard():
    if current_user.is_authenticated:
        logger.info("User is already authenticated. Loading home page.")
        return redirect('/')
    
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

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    redir = inverse_login_guard()
    if redir is not None: return redir

    form = SignupForm()

    if request.method == "GET":
        error_type = request.args.get('error')

        if error_type == None or error_type == '':
            error_message = ""
        elif str.find(error_type, "userexists") != -1:
            error_message = 'Username already exists. Please try another.'
            print(f"check: {error_type}")
        elif str.find(error_type, 'confirmpassword') != -1:
            error_message = 'Please confirm your password.'
        elif error_type:
            error_message = 'An unexpected error occurred. Please try again.'

        return render_template("authform.html", authaction="/signup", submitbtn_text="Sign up", form=form, error_message=error_message)

    if form.validate_on_submit():
        #todo - add to a handler
        username = str.lower(form.username.data)

        user = User.query.filter_by(username=username).first()

        if user:
            return redirect('/signup?error="userexists"')
        
        if form.confirm_password.data != form.password.data:
            return redirect('/signup?error="confirmpassword"')

        created_user = User(username=username, 
                            password=generate_password_hash(form.password.data))
        
        db.session.add(created_user)
        db.session.commit()

        login_user(created_user)
        return redirect('/newuser')
    
    return render_template("authform.html", authaction="/signup", submitbtn_text="Sign up", form=form, error_message="Unable to create account. Please try again.")

@login_manager.user_loader
def load_user(user_id):
    logger.debug(f"Attempting to load user with ID: {user_id}")
    return get_user_byid(user_id)