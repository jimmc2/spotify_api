import requests
from app.models import Song, Artist, Url, Genre, artistGenre
from app import app, db
import base64
import sys
import os
import json

class Spotify:
    def __init__(self):
        self.client_id = app.config['CLIENT_ID']
        self.client_secret = app.config['CLIENT_SECRET'] 
        self.auth_token = ''           
        self.get_headers = {"Authorization": "Bearer {}".format(self.auth_token),
                            "Accept": "application/json",
                            "Content-Type": "application/json"}
    

    def postAuth(self, id_, secret):
        post_headers = {}
        post_data = {'grant_type':'client_credentials'}
        auth_url = 'https://accounts.spotify.com/api/token'
        encode_header = base64.b64encode((id_ + ':' + secret).encode('ascii'))
        post_headers['Authorization'] =  'Basic ' + encode_header.decode('ascii')
        response = requests.post(auth_url, headers=post_headers,data=post_data)
        if response.status_code == 200:
            self.auth_token = response.json()['access_token']
            self.get_headers['Authorization'] =  "Bearer {}".format(self.auth_token)
 

    def get50artists(self):
        artists_ids = Artist.query.filter_by(popularity=None).limit(50).all()
        return artists_ids

    def get50songs(self):
        song_ids = Song.query.filter_by(popularity=None).limit(50).all()
        return song_ids ## returns list of song objects

    def queryArtists(self):
        artistList = self.get50artists()
        artist_ids = '%2C'.join([a.spotify_id for a in artistList])
        url = "https://api.spotify.com/v1/artists?ids=" + artist_ids
        response = requests.get(url,headers=self.get_headers)
        print(response)
        artists = response.json()['artists']
        keyps = ['genres','id','images','popularity']
        for artist in artists:
            for key in list(artist):
                if key not in keyps:
                    del artist[key]
        
        for i in range(len(artistList)):
            for j in range(len(artists)):
                if artistList[i].spotify_id == artists[j]['id']:
                    artistList[i].popularity = artists[j]['popularity']
                    if len([image for image in artists[j]['images'] if image['height']>=150 and image['height']<=300])>0:
                        artistList[i].image = [image for image in artists[j]['images'] if image['height']>=150 and image['height']<=300][-1]['url']
                    elif len(artists[j]['images'])>0:
                        artistList[i].image =  artists[j]['images'][-1]['url']
                    else:
                        pass
                    for genre in artists[j]['genres']:
                        dbgen = Genre.query.filter_by(name=genre).first() 
                        if dbgen:
                            artistList[i].genres.append(dbgen)
                        else:
                            gen = Genre(name=genre)
                            db.session.add(gen)
                            artistList[i].genres.append(gen)
        db.session.commit()

    def querySongs(self):
        songList = self.get50songs()
        song_ids = '%2C'.join([s.spotify_id for s in songList])
        url = "https://api.spotify.com/v1/tracks?ids=" + song_ids
        response = requests.get(url,headers=self.get_headers)
        tracks = response.json()['tracks']
        del_keys = ['available_markets','album','artists','disc_number','duration_ms','explicit','external_ids','href','is_local','name','preview_url','track_number','type','uri']
        
        for del_track in tracks:
            for dkey in del_keys:
                del del_track[dkey]

        for i in range(len(songList)):
            for j in range(len(tracks)):
                if songList[i].spotify_id == tracks[j]['id']:
                    songList[i].popularity = tracks[j]['popularity']  
                    db.session.flush()
        db.session.commit()