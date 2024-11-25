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
        validate: function () { $(this.id).val().length > 50; }
    },
    {
        id: '#bio',
        invalid_message: 'Bio cannot be longer than 1000 characters.',
        validate: function() { $(this.id).val().length > 1000; }
    },
    {
        id: '#password',
        invalid_message: 'placeholder',
        validate: function() { 
            if($(this.id).val().length < 8 )
                this.invalid_message = "Password must be at least 8 characters."
                return false;
        }
    }
];

$(document).ready(function () {

    fields.forEach(field => {
        $(field.id).on('change', function () {
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
        $(`${field.id}-error`).text('');
        $(`${field.id}-error`).hide();
        $('#settings-submit').removeAttr('disabled');
        return false;
    }

    $(field.id).addClass('is-invalid');
    $(`${field.id}-error`).text(field.invalid_message);
    $(`${field.id}-error`).show();
    $('#settings-submit').attr('disabled', 'disabled');

    return true;
}