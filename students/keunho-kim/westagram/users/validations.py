import re

from django.core.exceptions   import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_email(value):
    email_reg = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    regex = re.compile(email_reg)

    if regex.match(value):
        return True
    else:
        return False

def validate_phone(value):
    phone_reg = r"([0-9]{3}-[0-9]{4}-[0-9]{4})"
    regex = re.compile(phone_reg)

    if regex.match(value):
        return True
    else:
        return False

def validate_password(value):
    password_reg = r"([A-Za-z0-9@#$%^&+=]{8,})" #최소 8자리 이상, 대소문자 및 숫자 특수문자로 제한하나 어떤 조합 강제는 하지 않
    regex = re.compile(password_reg)

    if regex.match(value):
        return True
    else:
        return False
