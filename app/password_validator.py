from wtforms.validators import ValidationError

"""
ADAPTED FROM MY COURSEWORK ONE SUBMISSION

Flask WTForms validator for password fields.
Ensures a date is between a minimum and maximum date.

Follows the structure defined in other Flask Validators.
https://wtforms.readthedocs.io/en/2.3.x/validators/
"""
class PasswordValidator(object):
    def __init__(self, optional=False):
        self.optional = optional

    def __call__(self, form, field):
        self.validate_password(field.data)                                                                                                                                                          

    """
    Validation method for the Password.
    Ensures password meets requirements.
    """
    def validate_password(self, value):
        errors = []

        if self.optional and len(value) < 1:
            return

        if len(value) < 10:
            errors.append("Must be at least 10 characters.")

        if len(value) >= 50:
            errors.append("Must be less than 50 characters.")

        if not any(char.isupper() for char in value):
            errors.append("Must contain at least one capital letter.")

        if not any(char.isdigit() for char in value):
            errors.append("Must contain at least one number.")

        if not any(char in "~`!@#$%^&*()-_+={}[]|\\;:'\"<>,./?" for char in value):
            errors.append("Must contain at least one special character.")

        if len(errors) > 0:
            raise ValidationError(errors)