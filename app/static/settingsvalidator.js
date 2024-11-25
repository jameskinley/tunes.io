import { validatePassword } from "./passwordvalidator.js";

/**
 * CODE ADAPTED FROM MY COURSEWORK ONE 'modal.js'
 */

/**
 * The fields to be validated and the functions to do it.
 */
const fields = [
    {
        id: '#name',
        invalid_message: 'Name cannot be longer than 50 characters.',
        validate: function () {  let value = $(this.id).val(); return value.length >= 50; }
    },
    {
        id: '#bio',
        invalid_message: 'Bio cannot be longer than 1000 characters.',
        validate: function() { return $(this.id).val().length >= 1000; }
    },
    {
        id: '#settings-password',
        invalid_message: 'placeholder',
        validate: function() { 
            let value = $(this.id).val();
            
            if(value.length < 1) {
                return false;
            }

            this.invalid_message = validatePassword(value);
            return this.invalid_message.length > 0;
        }
    }
];

$(document).ready(function () {

    fields.forEach(field => {
        $(field.id).keyup(function () {
            field_validate(field);
        })
    })

    $('#settings-form').on('submit', function (event) {
        if (validate_fields()) {
            event.preventDefault();
        }
    });
});

/**
 * For each field, applies it's validator function.
 */
function validate_fields() {

    invalid = false;

    fields.forEach(field => {
        if(field_validate(field)) 
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
        $('#settings-submit').removeAttr('disabled');
        return false;
    }

    $(field.id).addClass('is-invalid');
    $(`${field.id}-error`).html(field.invalid_message);
    $(`${field.id}-error`).show();
    $('#settings-submit').attr('disabled', 'disabled');

    return true;
}