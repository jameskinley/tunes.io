from flask_login import UserMixin

class User(UserMixin):

    """
    Override of the default 'UserMixin' implemetation.
    Retrieves the user ID of the given user.
    """
    def get_id():
        "user guid"