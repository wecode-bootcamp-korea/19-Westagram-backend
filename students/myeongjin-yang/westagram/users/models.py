from django.db import models

class User(models.Model):
    email       = models.EmailField()
    phonenumber = models.CharField(max_length=15)
    password    = models.CharField(max_length=100)
    name        = models.CharField(max_length=45)
    username    = models.CharField(max_length=45)
    class Meta:
        db_table = 'users'