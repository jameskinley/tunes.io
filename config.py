import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

SPOTIFY_API_ID = os.getenv("SPOTIFY_API_ID")
SPOTIFY_API_SECRET = os.getenv("SPOTIFY_API_SECRET")
SPOTIFY_LOCALE = "GB"