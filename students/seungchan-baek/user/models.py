from django.db import models

class User(models.Model):
    email          = models.CharField(max_length=50)
    phone_number   = models.CharField(max_length=50)
    password       = models.CharField(max_length=500)
    name           = models.CharField(max_length=50)
    nickname       = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'
