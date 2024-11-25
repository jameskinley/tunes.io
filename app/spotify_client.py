import spotipy
from app import logging as logger
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_API_ID, SPOTIFY_API_SECRET, SPOTIFY_LOCALE
from .track import Track

"""
Leverages the spotify API to get information about tracks.
Uses the Spotipy library: https://spotipy.readthedocs.io/en/2.24.0/
Spotify API documentation: https://developer.spotify.com/documentation/web-api
"""
class SpotifyClient:

    """
    Initialises the class.
    """
    def __init__(self):
        cred_manager = SpotifyClientCredentials(client_id=SPOTIFY_API_ID, client_secret=SPOTIFY_API_SECRET)
        self.__spotify_client__ = spotipy.Spotify(client_credentials_manager=cred_manager)
    
    """
    Searches the Spotify track database for the given query.
    """
    def search(self, query):
        logger.debug(f"Fetching tracks from Spotify API for query: '{query}'")
        result = self.__spotify_client__.search(q=query, limit=5, market=SPOTIFY_LOCALE)
        
        tracks = []
        track_list = result['tracks']['items']

        for track in track_list:
            tracks.append(Track(track['id'],
                                track['name'],
                                track['artists'][0]['name'],
                                track['album']['name'],
                                track['album']['images'][1]['url'],
                                track['external_urls']['spotify']))
            
        logger.debug(f"Query returned {len(track)} tracks.")
        return tracks
    
    """
    Gets the track with the given track_id.
    """
    def get_track(self, track_id):
        track = self.__spotify_client__.track(track_id)
        return Track(track_id=track['id'],
                     title=track['name'],
                     artist=track['artists'][0]['name'],
                     album=track['album']['name'],
                     artwork=track['album']['images'][1]['url'],
                     url=track['external_urls']['spotify'])