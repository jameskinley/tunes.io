from .models import User

def get_user_byid(id):
    return User.query.filter_by(user_id=id).first()

def get_user_byusername(username):
    return User.query.filter_by(username=username).first()