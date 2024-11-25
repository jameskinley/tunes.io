export function validatePassword(value){
    let errors = "";

    if(value.length < 10) {
        errors += "&#8226; Must be at least 10 characters.<br>";
    }

    if(value.length >= 50) {
        errors += "&#8226; Must be less than 50 characters.<br>";
    }

    if(!value.match(/[A-Z]{1,}/)) {
        errors += "&#8226; Must contain at least one capital letter.<br>";
    }

    if(!value.match(/[0-9]{1,}/)) {
        errors += "&#8226; Must contain at least one number.<br>";
    }

    if(!value.match(/[~`!@#$%^&*()\-_+={}[\]|\\\;:"<>,./?]{1,}/)) {
        errors += "&#8226; Must contain at least one special character.<br>";
    }

    return errors;
}

export function confirmPassword(original, confirm){
    if(original.length < 1 || confirm.length < 1) {
        return false;
    } 
    return original != confirm;
}