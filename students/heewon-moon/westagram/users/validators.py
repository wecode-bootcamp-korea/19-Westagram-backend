import re

def password_validator(password):
    validator = re.compile('^(?=.*[A-Z])(?=.*[!@#$&*?])(?=.*[0-9])(?=.*[a-z])([\S]){8,}$')
    
    if validator.match(password):
        return True
    return False

def email_validator(email):
    validator = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    if validator.match(email):
        return True
    return False

def phone_validator(phone):
    validator = re.compile('^\d{9,11}$')
    if validator.match(phone):
        return True
    return False