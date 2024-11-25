from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import Length, ReadOnly
from app import logging as logger
from .user_repository import update_user

class SettingsForm(FlaskForm):

    username = StringField("Username")
    
    password = PasswordField("Password") #todo- custom validator
    confirmpassword = PasswordField("Confirm Password") #todo- custom validator

    name = StringField("Name")
    bio = TextAreaField("Bio", validators=[Length(max=1000)])

    def SetUserDefaults(self, user):
        self.username.data = f"@{user.username}"
        self.name.data = user.name
        self.bio.data = user.bio

    def Handler(self, current_user):
        if self.validate_on_submit():
            if not update_user(current_user.user_id, 
                        self.name.data, 
                        self.password.data, 
                        self.confirmpassword.data, 
                        self.bio.data):
                logger.error(f"Unable to update settings for user {current_user.user_id}")
                return False
            
            logger.debug("Saving Settings")
            return True
        
        logger.error(f"Unable to update settings for user {current_user.user_id}, the form was invalid.")
        return False