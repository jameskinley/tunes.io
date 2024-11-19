from app import db, logging as logger
from .models import Post
from .post_model import PostModel
from .spotify_client import SpotifyClient

def add_post(user_id, track_id, description):

    post = Post(user_id=user_id, track_id=track_id, description=description)
    db.session.add(post)

    logger.debug(f"Added post: {post}")

    db.session.commit()

def get_posts():
    post_raw =  Post.query.order_by(Post.post_id.desc())
    sp = SpotifyClient()
    posts = []

    for postr in post_raw:
        posts.append(PostModel(sp.get_track(postr.track_id), postr.user.username, postr.likes.count, postr.description))

    return posts