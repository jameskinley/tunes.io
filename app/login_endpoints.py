from app import app, login_manager, logging as logger
from .signup_form import SignupForm
from flask_login import current_user, logout_user
from flask import redirect, request, render_template
from .user_repository import UserRepository 
    
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
    
    form.loginHandler()

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
        elif str.find(error_type, 'confirmpassword') != -1:
            error_message = 'Please confirm your password.'
        elif error_type:
            error_message = 'An unexpected error occurred. Please try again.'

        return render_template("authform.html", authaction="/signup", submitbtn_text="Sign up", form=form, error_message=error_message)
    
    return form.signupHandler()

@login_manager.user_loader
def load_user(user_id):
    logger.debug(f"Attempting to load user with ID: {user_id}")
    repo = UserRepository()
    return repo.getUserById(user_id)