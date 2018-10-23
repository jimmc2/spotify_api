import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__)) 
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') #Uniform Resource Identifier
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')

