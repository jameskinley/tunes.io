export function validatePassword(value){
    let errors = "";

    if(value.length < 8) {
        errors += "Must be at least 8 characters.<br>";
    }

    if(!value.match(/[0-9]{1,}/)) {
        errors += "Must contain at least one number.<br>";
    }

    if(!value.match(/[~`!@#$%^&*()\-_+={}[\]|\\\;:"<>,./?]{1,}/)) {
        errors += "Must contain at least one special character.<br>";
    }

    return errors;
}