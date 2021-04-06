from django.db    import models
from django.forms import PasswordInput

class User(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.CharField(max_length=100)
    password     = models.TextField()
    phone_number = models.CharField(max_length=20)
    nickname     = models.CharField(max_length=20)

    class Meta:
        db_table = "users"
