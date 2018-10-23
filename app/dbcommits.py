from app import db
from app.models import Artist, Query , Song ##, Genre, ArtistImage
import datetime

class Payload:
    def __init__(self,dataObject):
        self.data = dataObject
        self.tracks = dataObject['tracks']
        # self.artist_spotify_id  = ''  ###determine artist
        self.artist_id = ''  ###primary artist

    def register_query(self): # Dependencies: Artist.id
        q = Query(date=datetime.datetime.now(), artist_id=self.artist_id, token=self.data['token'])
        db.session.add(q)

    def primary_artist(self):
        a = Artist.query.filter_by(spotify_id=self.data['artist']).first() 
        if a:
           self.artist_id = a.id
           self.artist_spotify_id = a.spotify_id
        else:
            a = Artist(name = self.data['tracks'][0]['artists'][0]['name'],spotify_id=self.data['artist'])
            db.session.add(a)
            db.session.flush()
            self.artist_id = a.id
            self.artist_spotify_id = a.spotify_id


    def add_new_song(self, trackObject):
        song = Song.query.filter_by(spotify_id=trackObject['id']).first()
        if song:
            pass
        else:
            song = Song(spotify_id= trackObject['id'], name=trackObject['name'], song_length=trackObject['duration_ms'],artist_id=self.artist_id)
            for performer_ in trackObject['artists'][1:]:
                song.performers.append(Artist.query.get(self.performer(performer_).id))
            db.session.add(song)
            db.session.flush()

    def all_songs(self):
        tracks = self.tracks
        for track in tracks:
            self.add_new_song(track)

    def performer(self,artistObject):
        p = Artist.query.filter_by(spotify_id=artistObject['spotify_id']).first()
        if p:
            return p
        else:
            p = Artist(name= artistObject['name'],spotify_id=artistObject['id'])
            db.session.add(p)
            db.session.flush()
            return p
    
    def commit(self):
        db.session.commit()