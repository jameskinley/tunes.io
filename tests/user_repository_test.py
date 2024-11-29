import pytest
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

            existing_user = User(user_id=1, username="existinguser", password=generate_password_hash("password"), name="initial", bio="initial")

            fuser1 = User(user_id=2, username="fuser1", password=generate_password_hash("password"))
            fuser2 = User(user_id=3, username="fuser2", password=generate_password_hash("password"))

            db.session.add(existing_user)
            db.session.add(fuser1)
            db.session.add(fuser2)

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
    def test_updateUser_withExistingUser_andValidDetails_updatesUser(self, repo, db_session):
        password = "newpassword"
        result = repo.updateUser(1, "name", password, password, "bio")

        user = db_session.query(User).filter_by(user_id=1).first()

        assert result
        assert user.name == "name"
        assert check_password_hash(user.password, password)
        assert user.bio == "bio"

    def test_updateUser_withNonExistantUser_returnsFalse(self, repo):
        result = repo.updateUser(999999, "name", "pword", "pword", "bio")
        assert not result

    def test_updateUser_withName_updatesNameOnly(self, repo, db_session):
        result = repo.updateUser(1, "newname", None, None, None)
        user = db_session.query(User).filter_by(user_id=1).first()

        assert result
        assert user.name == "newname"
        assert check_password_hash(user.password, "password")
        assert user.bio == "initial"

    def test_updateUser_withEmptyName_doesNotUpdateName(self, repo, db_session):
        result = repo.updateUser(1, "", None, None, None)
        user = db_session.query(User).filter_by(user_id=1).first()

        assert result
        assert user.name == "initial"

    def test_updateUser_withBio_updatesBioOnly(self, repo, db_session):
        result = repo.updateUser(1, None, None, None, "newbio")
        user = db_session.query(User).filter_by(user_id=1).first()

        assert result
        assert user.name == "initial"
        assert check_password_hash(user.password, "password")
        assert user.bio == "newbio"

    def test_updateUser_withEmptyBio_doesNotUpdateBio(self, repo, db_session):
        result = repo.updateUser(1, None, None, None, "")
        user = db_session.query(User).filter_by(user_id=1).first()

        assert result
        assert user.bio == "initial"

    def test_updatePassword_withConfirmPassword_updatesPasswordOnly(self, repo, db_session):
        result = repo.updateUser(1, None, "newpassword", "newpassword", None)
        user = db_session.query(User).filter_by(user_id=1).first()

        assert result
        assert check_password_hash(user.password, "newpassword")
        assert user.name == "initial"
        assert user.bio == "initial"

    def test_updatePassword_withExistingPassword_doesNotUpdatePassword(self, repo, db_session):
        result = repo.updateUser(1, None, "password", "password", None)
        user = db_session.query(User).filter_by(user_id=1).first()

        assert not result
        assert check_password_hash(user.password, "password")

    def test_updatePassword_withNoConfirmPassword_doesNotUpdatePassword(self, repo, db_session):
        result = repo.updateUser(1, None, "newpassword", "", None)
        user = db_session.query(User).filter_by(user_id=1).first()

        assert not result
        assert check_password_hash(user.password, "password")
    
    def test_updatePassword_withDifferentConfirmPassword_doesNotUpdatePassword(self, repo, db_session):
        result = repo.updateUser(1, None, "newpassword", "otherpassword", None)
        user = db_session.query(User).filter_by(user_id=1).first()

        assert not result
        assert check_password_hash(user.password, "password")

    """
    Set Follow tests.
    """
    def test_setFollow_true_withExistingUsername_createsFollow(self, repo, db_session):
        result = repo.setFollow(1, "fuser1", True)

        assert result
        assert db_session.query(Follow).filter_by(follower=1, followed=2).count() == 1

    def test_setFollow_false_withExistingUsername_removesFollow(self, repo, db_session):
        db_session.add(Follow(follower=1, followed=2))
        db_session.commit()

        result = repo.setFollow(1, "fuser1", False)

        assert result
        assert db_session.query(Follow).filter_by(follower=1, followed=2).count() == 0

    def test_setFollow_withUserIdMatchingUsername_returnsFalse(self, repo, db_session):
        result = repo.setFollow(1, "existinguser", True)

        assert not result
        assert db_session.query(Follow).filter_by(follower=1, followed=1).count() == 0

    def test_setFollow_withNonExistantUsername_returnsFalse(self, repo):
        assert not repo.setFollow(1, "idontexist", True)

    """
    Is Following tests.
    """
    def test_isFollowing_withExistingFollow_returnsTrue(self, repo, db_session):
        db_session.add(Follow(follower=1, followed=2))
        db_session.commit()

        assert repo.isFollowing(1, 2)

    def test_isFollowing_withNonExistantFollow_returnsFalse(self, repo, db_session):
        assert not repo.isFollowing(1, 2)