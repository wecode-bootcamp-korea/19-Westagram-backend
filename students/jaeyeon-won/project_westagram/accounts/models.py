from django.db import models

class User(models.Model):
    phone_number = models.CharField(max_length=20)
    email        = models.EmailField(max_length=100)
    name         = models.CharField(max_length=20)
    username     = models.CharField(max_length=40)
    password     = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'
# Create your models here.
