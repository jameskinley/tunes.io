"""
DTO For storing track search results.
"""
class Track:
    def __init__(self, track_id, title, artist, album):
        self.track_external_id = track_id
        self.title = title
        self.artist = artist
        self.album = album