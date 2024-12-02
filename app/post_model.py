"""
DTO for user posts.
"""
class PostModel:
    def __init__(self, user_liked, post_id, track, username, likes, description):
        self.user_liked = user_liked
        self.post_id = post_id
        self.track = track
        self.username = username
        self.likes = likes
        self.description = description