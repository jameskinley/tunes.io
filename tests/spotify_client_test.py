import pytest
from app.spotify_client import SpotifyClient
from unittest.mock import patch, MagicMock
from app.track import Track

@pytest.fixture
def spotify_client():
    return SpotifyClient()

@patch('app.spotify_client.spotipy.Spotify')
def test_search_returnsListOfTracks(mock_spotify, spotify_client):
    mock_spotify_instance = MagicMock()
    mock_spotify.return_value = mock_spotify_instance
    mock_spotify_instance.search.return_value = {
        'tracks': {
            'items': [
                {
                    'id': '123',
                    'name': 'Track 1',
                    'artists': [{'name': 'Artist 1'}],
                    'album': {'name': 'Album 1', 'images': [{'url': 'url1'}, {'url': 'url2'}]},
                    'external_urls': {'spotify': 'spotify_url_1'}
                },
                {
                    'id': '456',
                    'name': 'Track 2',
                    'artists': [{'name': 'Artist 2'}],
                    'album': {'name': 'Album 2', 'images': [{'url': 'url1'}, {'url': 'url2'}]},
                    'external_urls': {'spotify': 'spotify_url_2'}
                }
            ]
        }
    }

    spotify_client.__spotify_client__ = mock_spotify_instance
    
    tracks = spotify_client.search('test query')
    
    assert len(tracks) == 2
    assert isinstance(tracks[0], Track)
    assert tracks[0].track_external_id == '123'
    assert tracks[0].title == 'Track 1'
    assert tracks[0].artist == 'Artist 1'
    assert tracks[0].album == 'Album 1'
    assert tracks[0].artwork == 'url2'
    assert tracks[0].url == 'spotify_url_1'

@patch('app.spotify_client.spotipy.Spotify')
def test_get_track_returnsTrack(mock_spotify, spotify_client):
    mock_spotify_instance = MagicMock()
    mock_spotify.return_value = mock_spotify_instance
    mock_spotify_instance.track.return_value = {
        'id': '123',
        'name': 'Track 1',
        'artists': [{'name': 'Artist 1'}],
        'album': {'name': 'Album 1', 'images': [{'url': 'url1'}, {'url': 'url2'}]},
        'external_urls': {'spotify': 'spotify_url_1'}
    }
    
    spotify_client.__spotify_client__ = mock_spotify_instance
    track = spotify_client.get_track('123')
    
    assert isinstance(track, Track)
    assert track.track_external_id == '123'
    assert track.title == 'Track 1'
    assert track.artist == 'Artist 1'
    assert track.album == 'Album 1'
    assert track.artwork == 'url2'
    assert track.url == 'spotify_url_1'
