from flask import redirect, render_template
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length
from werkzeug.security import check_password_hash
from .user_repository import UserRepository
from .password_validator import PasswordValidator
from .username_validator import UsernameValidator

"""
Form to allow uses to login / signup.
"""
class SignupForm(FlaskForm):
    """
    Username input. Usernames must be a maximum of 50 characters, and be solely alphanumeric.
    """
    username = StringField('Username', validators=[DataRequired(), Length(max=50), UsernameValidator()])

    """
    Password input. Passwords must be at least 10 characters in length, have at least 1 capital letter, special character, and number.
    """
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=50), PasswordValidator()])

    """
    Confirm password input. Must match password when in use, but as this form is also used for login, this validation is done externally.
    """
    confirm_password = PasswordField('Confirm Password')

    """
    Indicates whether the session should remember a logged in user or not.
    """
    remember = BooleanField('Remember Me', default=False)

    def loginHandler(self):     
            username = str.lower(self.username.data)
            repo = UserRepository()
            user = repo.getUserByUsername(username)

            if not user or not check_password_hash(user.password, self.password.data):
                # Say incorrect login details regardless of whether account exists. This prevents bad actors from working out account names as easily.
                return render_template("authform.html", 
                                    authaction='/login', 
                                    submitbtn_text='Login', 
                                    form=self, 
                                    error_message="Incorrect login details. Please try again.")
            
            login_user(user, self.remember.data)
            return redirect('/')

    """
    Handles the sign-up logic. Returns a redirect / render request.
    """
    def signupHandler(self):
        if self.validate_on_submit():
            username = str.lower(self.username.data)
            repo = UserRepository()

            if self.confirm_password.data != self.password.data:
                return redirect('/signup?error="confirmpassword"')

            user = repo.createUser(username, self.password.data)

            if user == None:
                return redirect('/signup?error="userexists"')
            
            login_user(user)
            return redirect('/newuser')
            
        return render_template("authform.html", 
                               authaction="/signup", 
                               submitbtn_text="Sign up", 
                               form=self, 
                               error_message="Unable to create account. Please try again.")