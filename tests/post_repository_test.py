from unittest.mock import patch, MagicMock
import pytest
from app.models import User, Post, Like
from app.track import Track
from app.post_repository import db, PostRepository
from werkzeug.security import generate_password_hash, check_password_hash

class TestPostRepository:

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
            existing_post = Post(user_id=1, track_id="track1", description="this is a description")

            db.session.add(existing_user)
            db.session.add(existing_post)

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
        with patch("app.post_repository.SpotifyClient") as mock_spotify_client:
            mock_spotify_instance = MagicMock()
            mock_spotify_client.return_value = mock_spotify_instance

            mock_spotify_instance.get_track.side_effect = lambda track_id: Track(track_id, f"Track: {track_id}", "Artist", "Album", "Artwork", "Url")

            repo = PostRepository(mock_spotify_instance)
            return repo

    """
    Add Post tests. (Validation is handled outside of this class!)
    """
    def test_addPost_withValidData_addsPost(self, repo, db_session):
        repo.addPost(1, "trackid", "description")

        assert db_session.query(Post).filter_by(user_id=1, track_id="trackid", description="description").count() == 1

    """
    Get Posts tests.
    """
    def test_getPosts_withNoUserFilter_returnsAllPosts(self, repo, db_session):
        assert len(repo.getPosts(1)) == db_session.query(Post).count()

    def test_getPosts_withInvalidUserFilter_returnsNoPosts(self, repo):
        assert len(repo.getPosts(1, 9999)) == 0

    def test_getPosts_withUserFilter_returnsPostsByUser(self, repo, db_session):
        assert len(repo.getPosts(1, 1)) == db_session.query(Post).filter_by(user_id=1).count()

    """
    Set Like tests. Validation is expected to be handled outside of this class.
    """
    def test_setLike_true_addsLike(self, repo, db_session):
        assert repo.setLike(1, 1, True)
        assert db_session.query(Like).filter_by(user_id=1, post_id=1).count() == 1

    def test_setLike_false_removesLike(self, repo, db_session):
        db_session.add(Like(user_id=1, post_id=1))
        db_session.commit()

        result = repo.setLike(1, 1, False)

        assert result
        assert db_session.query(Like).filter_by(user_id=1, post_id=1).count() == 0

    def test_setLike_true_withNonExistantUserId_returnsFalse(self, repo):
        assert not repo.setLike(9999999, 1, True)

    def test_setLike_true_withNonExistantUserId_returnsFalse(self, repo):
        assert not repo.setLike(9999999, 1, False)

    def test_setLike_true_withNonExistantPostId_returnsFalse(self, repo):
        assert not repo.setLike(1, 999999, True)

    def test_setLike_false_withNonExistantPostId_returnsFalse(self, repo):
        assert not repo.setLike(1, 999999, False)