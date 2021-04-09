from django.db    import models
from .validations import validate_email, validate_password, validate_phone

class User(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.EmailField(max_length=100, validators=[validate_email], unique=True)
    password     = models.CharField(max_length=1000, validators=[validate_password])
    phone_number = models.CharField(max_length=20, validators=[validate_phone])
    nickname     = models.CharField(max_length=20)

    class Meta:
        db_table = "users"
