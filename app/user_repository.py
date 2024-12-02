from .models import User, Follow
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, logging as logger

"""
Contains methods for manipulating and querying user records.
"""
class UserRepository:

    def createUser(self, username, password):
        existing_user = self.getUserByUsername(username)

        if existing_user != None:
            logger.warning(f"Cannot create user. User with username '{username}' already exists.")
            return None
        
        logger.info(f"Creating user '{username}'")
        user = User(username=username, password=generate_password_hash(password))

        db.session.add(user)
        db.session.commit()

        logger.info(f"Successfully created user '{username}'")

        return user

    """
    Gets a user by the given ID.
    """
    def getUserById(self, id):
        return User.query.filter_by(user_id=id).first()

    """
    Gets a user by the given username.
    """
    def getUserByUsername(self, username):
        logger.debug(f"Searching for user '{username}'")
        return User.query.filter_by(username=username).first()

    """
    Updates a user with any changes found in the parameters of the method.
    """
    def updateUser(self, user_id, name, password, confirm_password, bio):
        user = self.getUserById(user_id)

        if user == None:
            logger.error("Could not locate user in database.")
            return False
        
        logger.debug(f"Making updates to user: '{user.username}'")
        
        if name != None and name != "" and user.name != name:
            logger.debug("Updating user name")
            user.name = name

        if bio != None and bio != "" and user.bio != bio:
            logger.debug("Updating user bio")
            user.bio = bio

        if confirm_password != password:
            logger.error("Unable to update user password. Passwords did not match.")
            return False
        elif password != None and confirm_password != None and password != "" and confirm_password != "":
            logger.debug("Updating user password")
            if check_password_hash(user.password, password):
                logger.error("Unable to update user password is same as existing password.")
                return False
            
            hash = generate_password_hash(password)
            user.password = hash

        db.session.commit()
        logger.debug(f"Successfully made updates to user '{user.username}'")
        return True

    """
    Creates/removes a following record from the user_id to the follow_username.
    """
    def setFollow(self, user_id, follow_username, state):
        follow_user = self.getUserByUsername(follow_username)

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

    """
    Returns a boolean value indicating whether the given user_id follows the follower_id or not.
    """
    def isFollowing(self, user_id, follower_id):
        return Follow.query.filter_by(follower=user_id ,followed=follower_id).first() != None