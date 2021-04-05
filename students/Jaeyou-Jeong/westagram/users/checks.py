import re

def email_validation(email):
    formula = re.compile('^[a-zA-z0-9-_.]+@+[a-zA-z0-9.]+\.+\w+$')

    if formula.match(email):
        return True

    return False

