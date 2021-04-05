import re

def email_validation(email):
    formula = re.compile('^[a-zA-Z0-9-_.]+@+[a-zA-Z0-9.]+\.+\w+$')

    if formula.match(email):
        return True

    return False

