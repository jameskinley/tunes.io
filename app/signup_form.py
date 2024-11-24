from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=100)])
    confirm_password = PasswordField('Confirm Password') #Shared - implement custom validation
    remember = BooleanField('Remember Me', default=False) #Shared - implement custom validation