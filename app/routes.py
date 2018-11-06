import sys
from app import app, db
from app.models import Artist, Genre, Performance, Song
from flask import render_template, url_for, redirect, flash, session, request, Response, make_response, jsonify
from app.dbcommits import Payload
import os
import time
import requests 
import json
import random
from app.backwork import Spotify
from app.forms import GenreForm, ArtistForm


@app.route('/')
def index():
    s = Spotify()
    s.postAuth(s.client_id,s.client_secret)
    s.queryArtists()
    s.querySongs()
    context={
        'access': s.auth_token
    }
    return render_template('index.html', **context)

@app.route('/genres')
def genre():
    form = GenreForm()
    context={
        'form': form
    }
    return render_template('genre.html', **context)

@app.route('/genres/<genre1>')
def genres(genre1):
    engine = db.engine
    connection = engine.connect()
    query ="""select gen.id, gen.name, gen2.id, gen2.name 
            from genre gen
            join artist_genre ag on gen.id=ag.genre_id
            join 
            (SELECT a.artist_id as a1, b.artist_id as a2, a.song_id from performance a
            join performance  b on a.song_id = b.song_id
            where a.artist_id <> b.artist_id and a.artist_id < b.artist_id) a 
            on ag.artist_id=a.a1
            join artist_genre ag2 on a.a2=ag2.artist_id
            join genre gen2 on ag2.genre_id=gen2.id
            where gen.id < gen2.id and gen.id <> gen2.id and (gen.id = {0} or gen2.id = {0})""".format(genre1)
    h = connection.execute(query)
    genreArray =[] 
    for row in h:
        if row[0] == int(genre1):
            genreArray.append((row[2],row[3]))
        else:
            genreArray.append((row[0],row[1]))
    connection.close()
    

    return jsonify({'genres':list(set(genreArray))})

@app.route('/artists')
def artist():
    form = ArtistForm()
    
    context={
        'form': form
    }
    return render_template('2artist.html', **context)

@app.route('/artists/<artist1>')
def artists(artist1):
    engine = db.engine
    connection = engine.connect()
    query ="""SELECT a.artist_id as a1, art1.name as a1_name, b.artist_id as a2, art2.name as a2_name, a.song_id from performance a
    join performance  b on a.song_id = b.song_id
    join artist art1 on a1=art1.id
    join artist art2 on a2=art2.id
    where a.artist_id <> b.artist_id and a.artist_id < b.artist_id and (a1 = {0} or a2 = {0})""".format(artist1)
    h = connection.execute(query)
    artistArray =[] 
    for row in h:
        if row[0] == int(artist1):
            artistArray.append((row[2],row[3]))
        else:
            artistArray.append((row[0],row[1]))
    connection.close()
    

    return jsonify({'artists':list(set(artistArray))})

@app.route('/artists/<artist1>_<artist2>')
def artistsSongs(artist1,artist2):
    engine = db.engine
    connection = engine.connect()
    query ="""Select p1.song_id
    FROM performance p1 
    JOIN performance p2 ON p1.song_id = p2.song_id 
    WHERE p1.artist_id <> p2.artist_id and p1.artist_id < p2.artist_id and 
    ((p1.artist_id = {0} and p2.artist_id = {1}) or (p1.artist_id = {1} and p2.artist_id = {0}))""".format(artist1,artist2)
    
    h = connection.execute(query)
    songs=[] 
    for id_ in h:
        songObject = {}
        song = Song.query.get(id_[0])
        songObject['name']=song.name
        songObject['artists']=[]
        artists = db.session.query(Artist).filter(Artist.id.in_([h.artist_id for h in song.Performers])).all()
        for art in artists:
            artistObject={}
            artistObject['name']=art.name
            artistObject['image']=art.image

            songObject['artists'].append(artistObject)
        songs.append(songObject)
    connection.close()

    return jsonify({'songs':songs})

@app.route('/receiver', methods = ['POST'])
def worker():
    data = request.get_json(silent=True)
    payload = Payload(data)
    payload.primary_artist()
    payload.register_query()
    payload.all_songs()
    payload.commit()
    print('received')
    context={
        'songs': data
    }
    return render_template('cars.html', **context)

@app.route('/svgtest')
def svg():
    headers = {'Content-Type': 'image/svg+xml'}
    return make_response(render_template('svg.html'),200,headers)