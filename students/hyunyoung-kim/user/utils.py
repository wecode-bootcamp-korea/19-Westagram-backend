import re

def validate_email(email):
    return re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None
    
def validate_password(password):
    MIN_LENGTH = 8
    return len(password) >= MIN_LENGTH 

