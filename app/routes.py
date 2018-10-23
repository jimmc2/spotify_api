import sys
from app import app, db
from app.models import Artist
from flask import render_template, url_for, redirect, flash, session, request, Response
from app.dbcommits import Payload
import os
import time
import requests
import base64 
import json
import random

@app.route('/')
def index():
    client_id = app.config['CLIENT_ID']
    client_secret = app.config['CLIENT_SECRET'] ### HIDE THIS SHIT IN ENV LATER
    url= 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'client_credentials'
    }
    def authcode(id_, secret):
        auth_header = base64.b64encode((id_ + ':' + secret).encode('ascii'))
        return 'Basic %s' % auth_header.decode('ascii')
    headers = {
        'Authorization': authcode(client_id,client_secret)
    }
    response = requests.post(url,headers=headers,data=data)
    context={
        'access': response.json()['access_token']
        # 'access': 'temp'
    }
    return render_template('index.html', **context)

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

