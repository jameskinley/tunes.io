from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import Length, ReadOnly, Optional
from app import logging as logger
from .post_repository import add_post

class SettingsForm(FlaskForm):

    username = StringField("Username", validators=[ReadOnly()])
    
    password = PasswordField("Password", validators=[]) #todo- custom validator
    confirmpassword = PasswordField("Confirm Password", validators=[]) #todo- custom validator

    name = StringField("Name", validators=[Optional()])
    bio = TextAreaField("Bio", validators=[Optional(), Length(max=1000)])

    def SetUserDefaults(self, user):
        self.username.data = f"@{user.username}"
        self.name.data = user.name
        self.bio.data = user.bio

    def Handler(self, current_user):
        if self.validate_on_submit():
            logger.debug("Saving Settings")