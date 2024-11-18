"""
DTO For storing track search results.
"""
class Track:
    def __init__(self, track_id, title, artist, album, artwork):
        self.track_external_id = track_id
        self.title = title
        self.artist = artist
        self.album = album
        self.artwork = artwork

    def to_dict(self): 
        return { 
            'track_external_id': self.track_external_id, 
            'title': self.title, 
            'artist': self.artist, 
            'album': self.album, 
            'artwork': self.artwork }