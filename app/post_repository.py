from app import db, logging as logger
from .models import Post, Like
from .post_model import PostModel
from .spotify_client import SpotifyClient

def add_post(user_id, track_id, description):

    post = Post(user_id=user_id, track_id=track_id, description=description)
    db.session.add(post)

    logger.debug(f"Added post: {post}")

    db.session.commit()

def get_posts(current_user_id, userfilter = None):

    if userfilter == None:
        post_raw =  Post.query.order_by(Post.post_id.desc())
    else:
        post_raw = Post.query.filter_by(user_id=userfilter).order_by(Post.post_id.desc())

    sp = SpotifyClient()
    posts = []

    for postr in post_raw:
        track = sp.get_track(postr.track_id)
        logger.debug(f"Got track: {track.to_dict()}")
        posts.append(PostModel(any(like.user_id == current_user_id for like in postr.likes), 
                               postr.post_id, track, 
                               postr.user.username, 
                               postr.likes.count(), 
                               postr.description))

    return posts

def set_like(user_id, post_id, state):
    logger.debug(f"Setting post {post_id} to like state {state}")

    if state:
        like = Like(user_id=user_id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return
    
    existing_like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()

    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()