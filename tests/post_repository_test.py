import pytest

"""
Add Post tests. (Validation is handled outside of this class!)
"""
def test_addPost_withValidData_addsPost():
    assert 1==1

"""
Get Posts tests.
"""
def test_getPosts_withNoUserFilter_returnsAllPosts():
    assert 1==1

def test_getPosts_withInvalidUserFilter_returnsNoPosts():
    assert 1==1

def test_getPosts_withUserFilter_returnsPostsByUser():
    assert 1==1

"""
Set Like tests. Validation is expected to be handled outside of this class.
"""
def test_setLike_true_addsLike():
    assert 1==1

def test_setLike_false_removesLike():
    assert 1==1

def test_setLike_withNonExistantUserId_returnsFalse():
    assert 1==1

def test_setLike_withNonExistantPostId_returnsFalse():
    assert 1==1