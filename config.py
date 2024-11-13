import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

SPOTIFY_API_ID = "40cf6eca2ed24e5ba0040de7dc954267"
SPOTIFY_API_SECRET = "f5d738d86f0744a5b044b020ba5cbfe3" #If we have scope this should be hidden away
SPOTIFY_LOCALE = "GB"