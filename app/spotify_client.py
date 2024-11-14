import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_API_ID, SPOTIFY_API_SECRET, SPOTIFY_LOCALE
from .track import Track

class SpotifyClient:

    def __init__(self):
        cred_manager = SpotifyClientCredentials(client_id=SPOTIFY_API_ID, client_secret=SPOTIFY_API_SECRET)
        self.__spotify_client__ = spotipy.Spotify(client_credentials_manager=cred_manager)
    
    def search(self, query):
        result = self.__spotify_client__.search(q=query, limit=5, market=SPOTIFY_LOCALE)
        
        tracks = []
        track_list = result['tracks']['items']

        for track in track_list:
            print(track)
            tracks.append(Track(album=track['album']['name'], title=track['name'], artist=track['artists'][0]['name'], track_id=track['id'], artwork=track['album']['images'][1]['url']))

        return tracks