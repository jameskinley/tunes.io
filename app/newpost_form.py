from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length
from app import logging as logger
from .post_repository import PostRepository

"""
Form for creating a new post.
"""
class PostForm(FlaskForm):
    """
    The external spotify track_id used to get data about the track.
    """
    track_id = HiddenField("track_id", validators=[DataRequired(), Length(max=1000)])

    """
    The user-entered post description.
    """
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=1000)])

    """
    Handles form submission.
    """
    def Handler(self, current_user):
        if self.validate_on_submit():
            logger.debug("Adding post.")
            repo = PostRepository()
            repo.addPost(current_user.user_id, track_id=self.track_id.data, description=self.description.data)
        else:
            logger.debug("Cannot add post: form invalid.")