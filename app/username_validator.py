from wtforms.validators import ValidationError

"""
ADAPTED FROM MY COURSEWORK ONE SUBMISSION

Flask WTForms validator for username fields.

Follows the structure defined in other Flask Validators.
https://wtforms.readthedocs.io/en/2.3.x/validators/
"""
class UsernameValidator(object):
    def __init__(self):
        pass

    def __call__(self, form, field):
        self.validate_username(field.data)                                                                                                                                                          

    """
    Validation method for the Username.
    Ensures username only has valid characters (alphanumeric).
    """
    def validate_username(self, value):
        errors = []

        if len(value) >= 50:
            errors.append("Must be less than 50 characters.")

        if not value.isalnum():
            errors.append("Must be letters and numbers only.")

        if len(errors) > 0:
            raise ValidationError(errors)