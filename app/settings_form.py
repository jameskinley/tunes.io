from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import Length
from app import logging as logger
from .user_repository import UserRepository
from .password_validator import PasswordValidator

"""
Form for updating user settings.
"""
class SettingsForm(FlaskForm):

    """
    Username field. This is readonly and purely for aesthetics.
    """
    username = StringField("Username")
    
    """
    Password input.
    """
    password = PasswordField(label="Password", validators=[PasswordValidator(optional=True)])

    """
    Confirm password input.
    """
    confirmpassword = PasswordField(label="Confirm Password")

    """
    Name input.
    """
    name = StringField("Name", validators=[Length(max=30)])

    """
    Bio input.
    """
    bio = TextAreaField("Bio", validators=[Length(max=1000)])

    """
    Pre-populates the fields with existing values pertaining to the user, if available.
    """
    def SetUserDefaults(self, user):
        self.username.data = f"@{user.username}"
        self.name.data = user.name
        self.bio.data = user.bio

    """
    Handles updates to the user.
    """
    def Handler(self, current_user):
        if self.validate_on_submit():
            repo = UserRepository()
            if not repo.updateUser(current_user.user_id, 
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