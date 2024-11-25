from .models import User, Follow
from app import db, logging as logger

def get_user_byid(id):
    return User.query.filter_by(user_id=id).first()

def get_user_byusername(username):
    return User.query.filter_by(username=username).first()

def set_follow(user_id, follow_username, state):
    follow_user = get_user_byusername(follow_username)

    if follow_user == None:
        logger.error("Cannot follow user that doesn't exist")
        return False
    
    if follow_user.user_id == user_id:
        logger.error("Cannot self-follow.")
        return False

    logger.debug(f"Setting follow state between {user_id} and {follow_user.user_id} as {state}")

    current_follow = Follow.query.filter_by(follower=user_id ,followed=follow_user.user_id).first()
    
    if state and current_follow == None:
        new_follow = Follow(follower=user_id, followed=follow_user.user_id)
        db.session.add(new_follow)
        db.session.commit()
        return True
    
    if current_follow != None:
        db.session.delete(current_follow)
        db.session.commit()

    return True

def is_following(user_id, follower_id):
    if Follow.query.filter_by(follower=user_id ,followed=follower_id).first() != None:
        return True
    return False