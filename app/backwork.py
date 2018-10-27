import requests
from app.models import Song, Artist, Url, Genre, artistGenre
from app import db

class sleeperQuery:
    def __init__(self):
        self.headers= {"Authorization": "",
                        "Accept": "application/json",
                        "Content-Type": "application/json"} 

    # def authcode(id_, secret):
    #     auth_header = base64.b64encode((id_ + ':' + secret).encode('ascii'))
    #     return 'Basic %s' % auth_header.decode('ascii')
    # headers = {
    #     'Authorization': authcode(client_id,client_secret)
    # }
    # response = requests.post(url,headers=headers,data=data)

    def get50artists(self):
        artists_ids = Artist.query.filter_by(popularity=None).limit(50).all()
        return artists_ids

    def get50songs(self):
        song_ids = Song.query.filter_by(popularity=None).limit(50).all()
        return song_ids ## returns list of song objects

    def queryArtists(self,artistList):
        artist_ids = '%2C'.join([a.spotify_id for a in artistList])
        url = "https://api.spotify.com/v1/artists?ids=" + artist_ids
        response = requests.get(url,headers=self.headers)
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

    def querySong(self,songList):
        song_ids = '%2C'.join([s.spotify_id for s in songList])
        url = "https://api.spotify.com/v1/tracks?ids=" + song_ids
        response = requests.get(url,headers=self.headers)
        tracks = response.json()['tracks']
        del_keys = ['available_markets','album','artists','disc_number','duration_ms','explicit','external_ids','href','is_local','name','preview_url','track_number','type','uri']
        
        for del_track in tracks:
            for dkey in del_keys:
                del del_track[dkey]

        for i in range(len(songList)):
            for j in range(len(tracks)):
                if songList[i].spotify_id == tracks[j]['id']:
                    songList[i].popularity = tracks[j]['popularity']
                    for k,v in tracks[j]['external_urls'].items():
                        print(k)
                        if k == 'spotify':
                            pass
                        else:
                            url = Url(song_id=songList[i].id,site=k,link=v)
                            print('url')
                            db.session.add(url)           
                    db.session.flush()
        db.session.commit()