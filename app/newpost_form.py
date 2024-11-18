from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ReadOnly

class PostForm(FlaskForm):
    track_id = HiddenField("track_id", validators=[DataRequired(), Length(max=1000), ReadOnly()])
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=1000)])