import re

from .models   import User 

def email_check(email):
    return re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) != None 

def password_check(password):
    return len(password)>=8

def duplicate_email_check(email):
    return User.objects.filter(email=email).exists() 
    
def duplicate_nickname_check(nickname):
    return User.objects.filter(nickname=nickname).exists()