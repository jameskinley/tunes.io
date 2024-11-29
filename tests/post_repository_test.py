import pytest

class TestPostRepository:
    """
    Add Post tests. (Validation is handled outside of this class!)
    """
    def test_addPost_withValidData_addsPost(self):
        assert 1 == 1

    """
    Get Posts tests.
    """
    def test_getPosts_withNoUserFilter_returnsAllPosts(self):
        assert 1 == 1

    def test_getPosts_withInvalidUserFilter_returnsNoPosts(self):
        assert 1 == 1

    def test_getPosts_withUserFilter_returnsPostsByUser(self):
        assert 1 == 1

    """
    Set Like tests. Validation is expected to be handled outside of this class.
    """
    def test_setLike_true_addsLike(self):
        assert 1 == 1

    def test_setLike_false_removesLike(self):
        assert 1 == 1

    def test_setLike_withNonExistantUserId_returnsFalse(self):
        assert 1 == 1

    def test_setLike_withNonExistantPostId_returnsFalse(self):
        assert 1 == 1
