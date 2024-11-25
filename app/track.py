from app import logging as logger
"""
DTO For storing track search results.
"""
class Track:
    """
    Initialises the track DTO.
    """
    def __init__(self, track_id, title, artist, album, artwork, url):
        self.track_external_id = track_id
        self.title = title
        self.artist = artist
        self.album = album
        self.artwork = artwork
        self.url = url

    """
    Converts the track to a dictionary format.
    """
    def to_dict(self):
        return { 
            'track_external_id': self.track_external_id, 
            'title': self.title, 
            'artist': self.artist, 
            'album': self.album, 
            'artwork': self.artwork,
            'url': self.url 
        }