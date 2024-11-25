import { validatePassword } from "./passwordvalidator.js";

/**
 * CODE ADAPTED FROM MY COURSEWORK ONE 'modal.js'
 */

/**
 * The fields to be validated and the functions to do it.
 */
const fields = [
    {
        id: '#username',
        invalid_message: 'Username must be less than 50 characters.',
        validate: function() {
            let value = $(this.id).val();
            if (value.length >= 50) {
                return true;
            }
            return false;
        }
    },
    {
        id: '#password',
        invalid_message: 'placeholder',
        validate: function () {
            let value = $(this.id).val();

            if (value.length < 1) {
                return false;
            }

            this.invalid_message = validatePassword(value);
            return this.invalid_message.length > 0;
        }
    },
    {
        id: '#confirm_password',
        invalid_message: "The passwords do not match.",
        validate: function () {
            let confirmValue = $(this.id).val();

            if (confirmValue.length < 1) {
                this.invalid_message = "Please confirm your password.";
                return false;
            }

            this.invalid_message = "The passwords do not match.";
            let mainValue = $('#password').val();
            return confirmValue != mainValue;
        }
    }
];

$(document).ready(function () {
    if ($('#auth-form').attr('action') == '/signup') {
        fields.forEach(field => {
            $(field.id).keyup(function () {
                field_validate(field);
            })
        });

        $('#auth-form').on('submit', function (event) {
            if (validate_fields()) {
                event.preventDefault();
            }
        });
    }
});

/**
 * For each field, applies it's validator function.
 */
function validate_fields() {
    let invalid = false;

    fields.forEach(field => {
        if (field_validate(field))
            invalid = true;
    });

    return invalid;
}

/**
 * Validates a single @param field
 */
function field_validate(field) {
    if (!field.validate()) {
        $(field.id).removeClass('is-invalid');
        $(`${field.id}-error`).html('');
        $(`${field.id}-error`).hide();
        $('#auth-submit').removeAttr('disabled');
        return false;
    }

    $(field.id).addClass('is-invalid');
    $(`${field.id}-error`).html(field.invalid_message);
    $(`${field.id}-error`).show();
    $('#auth-submit').attr('disabled', 'disabled');

    return true;
}