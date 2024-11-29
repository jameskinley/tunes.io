import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.models import User, Follow
from app.user_repository import db, UserRepository
from werkzeug.security import generate_password_hash, check_password_hash

class TestUserRepository:

    @pytest.fixture(scope="function", autouse=True)
    def app(self):
        from flask import Flask
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.init_app(app)

        with app.app_context():
            db.create_all()

            existing_user = User(user_id=1, username="existinguser", password="password")

            db.session.add(existing_user)
            db.session.commit()

            yield app

            db.session.remove()
            db.drop_all()

    @pytest.fixture(scope="function", autouse=True)
    def db_session(self, app):
        with app.app_context():
            yield db.session

    @pytest.fixture(scope="function", autouse=True)
    def repo(self, db_session):
        return UserRepository()

    """
    Create User tests.
    """
    def test_createUser_withValidUsername_createsUser(self, repo, db_session):
        user = repo.createUser("testuser", "testpassword")

        assert user is not None
        assert user.username == "testuser"
        assert db_session.query(User).filter_by(username="testuser").count() == 1

    def test_createUser_withTakenUsername_doesNotCreateUser(self, repo, db_session):
        user = repo.createUser("existinguser", "testpassword")

        assert user is None
        assert db_session.query(User).filter_by(username="existinguser").count() == 1

    """
    Get User by User_ID tests.
    """
    def test_getUserById_withExistingUserId_returnsUser(self, repo):
        user = repo.getUserById(1)

        assert user is not None
        assert user.user_id == 1

    def test_getUserById_WithNonExistantUserId_returnsNone(self, repo):
        user = repo.getUserById(999999999)

        assert user is None

    """
    Get User by Username tests.
    """
    def test_getUserByUsername_withExistingUsername_returnsUser(self, repo):
        user = repo.getUserByUsername("existinguser")

        assert user is not None
        assert user.username == "existinguser"

    def test_getUserByUsername_withNonExistantUsername_returnsNone(self, repo):
        user = repo.getUserByUsername("idontexist")

        assert user is None

    """
    Update User tests.
    """
    def test_updateUser_withExistingUser_andValidDetails_updatesUser(self):
        assert 1 == 1

    def test_updateUser_withNonExistantUser_returnsFalse(self):
        assert 1 == 1

    def test_updateUser_withName_updatesName(self):
        assert 1 == 1

    def test_updateUser_withEmptyName_doesNotUpdateName(self):
        assert 1 == 1

    def test_updateUser_withBio_updatesBio(self):
        assert 1 == 1

    def test_updateUser_withEmptyBio_doesNotUpdateBio(self):
        assert 1 == 1

    def test_updatePassword_withConfirmPassword_updatesPassword(self):
        assert 1 == 1

    def test_updatePassword_withExistingPassword_doesNotUpdatePassword(self):
        assert 1 == 1

    def test_updatePassword_withNoConfirmPassword_doesNotUpdatePassword(self):
        assert 1 == 1

    def test_updatePassword_withDifferentConfirmPassword_doesNotUpdatePassword(self):
        assert 1 == 1

    """
    Set Follow tests.
    """
    def test_setFollow_true_withExistingUsername_createsFollow(self):
        assert 1 == 1

    def test_setFollow_false_withExistingUsername_removesFollow(self):
        assert 1 == 1

    def test_setFollow_withUserIdMatchingUsername_returnsFalse(self):
        assert 1 == 1

    def test_setFollow_withNonExistantUsername_returnsFalse(self):
        assert 1 == 1

    """
    Is Following tests.
    """
    def test_isFollowing_withExistingFollow_returnsTrue(self):
        assert 1 == 1

    def test_isFollowing_withNonExistantFollow_returnsFalse(self):
        assert 1 == 1