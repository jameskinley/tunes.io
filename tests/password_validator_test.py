import pytest
from app.password_validator import PasswordValidator, ValidationError

@pytest.fixture
def validator():
    return PasswordValidator()

def test_validatePassword_with51CharPassword_raisesError(validator):
    with pytest.raises(ValidationError, match="Must be less than 50 characters."):
        password = 'a' * 51
        validator.validate_password(password)

def test_validatePassword_with9CharPassword_raisesError(validator):
    with pytest.raises(ValidationError, match="Must be at least 10 characters."):
        password = 'a' * 9
        validator.validate_password(password)

def test_validatePassword_withAllLowerCase_raisesError(validator):
    with pytest.raises(ValidationError, match="Must contain at least one capital letter."):
        password = 'a' * 10
        validator.validate_password(password)

def test_validatePassword_withNoDigits_raisesError(validator):
    with pytest.raises(ValidationError, match="Must contain at least one number."):
        password = 'A' * 10
        validator.validate_password(password)

def test_validatePassword_withNoSpecialChar_raisesError(validator):
    with pytest.raises(ValidationError, match="Must contain at least one special character."):
        password = 'A1bcdefgh'
        validator.validate_password(password)

def test_validatePassword_withValidPassword_doesNotRaiseError(validator):
    password = 'A1bcdefgh!'
    validator.validate_password(password)