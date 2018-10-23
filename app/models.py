from app import db

# artistGenre = db.Table('artist_genre',
#     db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'),primary_key=True),
#     db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'),primary_key=True)
# )

association_table = db.table('association',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'),primary_key=True),
    db.Column('performer_id', db.Integer, db.ForeignKey('artist.id'),primary_key=True)
)    

class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer,primary_key=True)
    spotify_id = db.Column(db.String, unique=True) 
    name = db.Column(db.String)
    popularity = db.Column(db.Integer)
    queries = db.relationship('Query', backref='artists', lazy='dynamic')
    songs = db.relationship('Song', backref='artist', lazy='dynamic')
    # genre = db.relationship('Genre', secondary=artistGenre, lazy='dynamic', backref=db.backref('artists', lazy='dynamic'))
    # artist_image = db.relationship('ArtistImage', backref='artist', lazy='dynamic')

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
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    performers = db.relationship('Artist', secondary=association_table,backref='performances')
    
# class Genre(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.String)


# class ArtistImage(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
#     img_url = db.Column(db.String)


