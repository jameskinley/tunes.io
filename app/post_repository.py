from app import db, logging as logger
from .models import Post, Like
from .post_model import PostModel
from .user_repository import UserRepository
from .spotify_client import SpotifyClient

"""
Contains methods for manipulating and querying Post records.
"""
class PostRepository():

    def __init__(self, spotifyClient = SpotifyClient()):
        self.sp = spotifyClient

    """
    Creates a new post for the given user_id, with the track_id and description provided.
    """
    def addPost(self, user_id, track_id, description):

        post = Post(user_id=user_id, track_id=track_id, description=description)
        db.session.add(post)

        logger.debug(f"Added post: {post}")

        db.session.commit()

    """
    Gets a list of all posts. Can be filtered by user_id.
    """
    def getPosts(self, current_user_id, userfilter = None):

        if userfilter == None:
            post_raw =  Post.query.order_by(Post.post_id.desc())
        else:
            post_raw = Post.query.filter_by(user_id=userfilter).order_by(Post.post_id.desc())
        posts = []

        for postr in post_raw:
            track = self.sp.get_track(postr.track_id)
            logger.debug(f"Got track: {track.to_dict()}")
            posts.append(PostModel(any(like.user_id == current_user_id for like in postr.likes), 
                                postr.post_id, track, 
                                postr.user.username, 
                                postr.likes.count(), 
                                postr.description))

        return posts

    """
    Sets the post with 'post_id' to the given like 'state' for the given 'user_id'.
    """
    def setLike(self, user_id, post_id, state):
        logger.debug(f"Setting post {post_id} to like state {state}")

        userRepo = UserRepository()
        if userRepo.getUserById(user_id) == None:
            logger.error(f"Cannot set post like. User ID '{user_id}' does not exist.")
            return False

        if Post.query.filter_by(post_id=post_id).first() == None:
            logger.error(f"Cannot set post like. Post ID '{post_id}' does not exist.")
            return False

        if state:
            like = Like(user_id=user_id, post_id=post_id)
            db.session.add(like)
            db.session.commit()
            return True
        
        existing_like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()

        if existing_like:
            db.session.delete(existing_like)
            db.session.commit()

        return True