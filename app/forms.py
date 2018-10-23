from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class ArtistForm(FlaskForm):
    artist = StringField('Artist', validators = [DataRequired()])