from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length
from app import logging as logger
from .post_repository import add_post

class PostForm(FlaskForm):
    track_id = HiddenField("track_id", validators=[DataRequired(), Length(max=1000)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=1000)])

def post_form_handler(form, current_user):
    if form.validate_on_submit():
        logger.debug("Adding post.")
        add_post(current_user.user_id, track_id=form.track_id.data, description=form.description.data)
    else:
        logger.debug("Form invalid.")