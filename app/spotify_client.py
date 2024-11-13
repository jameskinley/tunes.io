import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_API_ID, SPOTIFY_API_SECRET, SPOTIFY_LOCALE
from .track import Track

class SpotifyClient:

    def __init__(self):
        cred_manager = SpotifyClientCredentials(client_id=SPOTIFY_API_ID, client_secret=SPOTIFY_API_SECRET)
        self.__spotify_client__ = spotipy.Spotify(client_credentials_manager=cred_manager)
    
    def search(self, query):
        raw_results = self.__spotify_client__.search(q=query, limit=5, market=SPOTIFY_LOCALE)

        if(len(raw_results) < 1):
            return None
        
        tracks = []
        for result in raw_results:
            track = result['tracks']['items']
            tracks.append(Track(album=track['album']['name'], title=track['name'], artist=track['artists'][0]['name'], track_id=track['id']))
        return tracks