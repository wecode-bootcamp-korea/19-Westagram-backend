import re

def validator_password(password):
    validator = re.compile('^(?=.*[A-Z])(?=.*[!@#$&*?])(?=.*[0-9])(?=.*[a-z])([\S]){8,}$')

    if validator.match(password):
        return True
    return False

def validator_email(email):
    validator = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    if validator.match(email):
        return True
    return False

def validator_number(number):
    validator = re.compile('^\d{9,11}$')

    if validator.match(number):
        return True
    return False
