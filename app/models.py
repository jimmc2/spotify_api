from app import db

artistGenre = db.Table('artist_genre',
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'),primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'),primary_key=True)
)

class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer,primary_key=True)
    spotify_id = db.Column(db.String, unique=True) 
    name = db.Column(db.String)
    popularity = db.Column(db.Integer)
    image = db.Column(db.String)  #url to small spotify image
    queries = db.relationship('Query', backref='artists', lazy='dynamic')
    genres = db.relationship("Genre", secondary=artistGenre, backref='artists')


class Query(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    token = db.Column(db.String)

class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer,primary_key=True)
    spotify_id = db.Column(db.String, unique=True) 
    name = db.Column(db.String) 
    song_length =  db.Column(db.Integer)
    popularity =  db.Column(db.Integer)
    urls = db.relationship('Url', lazy='dynamic')

class Url(db.Model):
    __tablename__ = 'external_url'
    id = db.Column(db.Integer,primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    site = db.Column(db.String) 
    link = db.Column(db.String) 

class Performance(db.Model):
    __tablename__ = 'performance'
    id = db.Column(db.Integer,primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    is_primary = db.Column(db.Boolean)
    artist = db.relationship(Artist, backref='Performances')
    song = db.relationship(Song, backref='Performers')    
    
class Genre(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)




