from django.db import models

class User(models.Model):
    email        = models.CharField(max_length=128) 
    password     = models.CharField(max_length=64)
    name         = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=64)

    class Meta:
        db_table = 'users'


