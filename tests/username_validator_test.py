import pytest
from app.username_validator import UsernameValidator, ValidationError

@pytest.fixture
def validator():
    return UsernameValidator()

def test_validate_username_with51CharUsername_raisesError(validator):
    with pytest.raises(ValidationError, match="Must be less than 50 characters."):
        username = 'a' * 51
        validator.validate_username(username)

def test_validate_username_withOnlySpecialCharUsername_raisesError(validator):
    with pytest.raises(ValidationError, match="Must be letters and numbers only."):
        username = '!' * 10
        validator.validate_username(username)

def test_validate_username_withContainingSpecialCharUsername_raisesError(validator):
    with pytest.raises(ValidationError, match="Must be letters and numbers only."):
        username = 'a123!'
        validator.validate_username(username)

def test_validate_username_withLongSpecialCharUsername_raisesError(validator):
    with pytest.raises(ValidationError, match="['Must be less than 50 characters.', 'Must be letters and numbers only.']"):
        username = 'a!' * 29
        validator.validate_username(username)

def test_validate_username_withValidUsername_doesNotRaiseError(validator):
    username = "a" * 49
    validator.validate_username(username)