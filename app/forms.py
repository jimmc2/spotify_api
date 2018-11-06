from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Genre, Artist, Performance, Song
from app import db

class GenreForm(FlaskForm):
    
    genre1 = SelectField('Genre1', validators=[DataRequired()], coerce=int, choices=[(i.id, i.name) for i in Genre.query.all()])
    genre2 = SelectField('Genre2', choices='', coerce=int)

primary_artists = db.select([Performance.artist_id]).where(Performance.is_primary == 1)

class ArtistForm(FlaskForm):
    artist1 = SelectField('artist1', validators=[DataRequired()], coerce=int, choices=[i for i in Performance.query.join(Artist,Performance.artist_id==Artist.id).with_entities(Performance.artist_id,Artist.name).group_by(Performance.artist_id).all()])
    # artist1 = SelectField('artist2', choices='', coerce=int)
    artist2 = SelectField('artist2', choices='', coerce=int)
