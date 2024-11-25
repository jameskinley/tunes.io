from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

"""
Form to allow uses to login / signup.
"""
class SignupForm(FlaskForm):
    """
    Username input.
    """
    username = StringField('Username', validators=[DataRequired(), Length(max=100)])

    """
    Password input. Passwords must be at least 10 characters in length, have at least 1 capital letter, special character, and number.
    """
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=100)]) #todo add complexity validator

    """
    Confirm password input. Must match password when in use, but as this form is also used for login, this validation is done externally.
    """
    confirm_password = PasswordField('Confirm Password')

    """
    Indicates whether the session should remember a logged in user or not.
    """
    remember = BooleanField('Remember Me', default=False)