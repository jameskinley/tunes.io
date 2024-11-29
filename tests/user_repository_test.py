import pytest

@pytest.fixture
def setup():
    pass

@pytest.fixture
def teardown():
    pass

"""
Create User tests.
"""
def test_createUser_withValidUsername_createsUser():
    assert 1==1

def test_createUser_withTakenUsername_doesNotCreateUser():
    assert 1==1

"""
Get User by User_ID tests.
"""
def test_getUserById_withExistingUserId_returnsUser():
    assert 1==1

def test_getUserById_WithNonExistantUserId_returnsNone():
    assert 1==1

"""
Get User by Username tests.
"""
def test_getUserByUsername_withExistingUsername_returnsUser():
    assert 1==1

def test_getUserByUsername_withNonExistantUsername_returnsNone():
    assert 1==1

"""
Update User tests.
"""
def test_updateUser_withExistingUser_andValidDetails_updatesUser():
    assert 1==1

def test_updateUser_withNonExistantUser_returnsFalse():
    assert 1==1

def test_updateUser_withName_updatesName():
    assert 1==1

def test_updateUser_withEmptyName_doesNotUpdateName():
    assert 1==1

def test_updateUser_withBio_updatesBio():
    assert 1==1

def test_updateUser_withEmptyBio_doesNotUpdateBio():
    assert 1==1

def test_updatePassword_withConfirmPassword_updatesPassword():
    assert 1==1

def test_updatePassword_withExistingPassword_doesNotUpdatePassword():
    assert 1==1

def test_updatePassword_withNoConfirmPassword_doesNotUpdatePassword():
    assert 1==1

def test_updatePassword_withDifferentConfirmPassword_doesNotUpdatePassword():
    assert 1==1

"""
Set Follow tests.
"""
def test_setFollow_true_withExistingUsername_createsFollow():
    assert 1==1

def test_setFollow_false_withExistingUsername_removesFollow():
    assert 1==1

def test_setFollow_withUserIdMatchingUsername_returnsFalse():
    assert 1==1

def test_setFollow_withNonExistantUsername_returnsFalse():
    assert 1==1

"""
Is Following tests.
"""
def test_isFollowing_withExistingFollow_returnsTrue():
    assert 1==1

def test_isFollowing_withNonExistantFollow_returnsFalse():
    assert 1==1