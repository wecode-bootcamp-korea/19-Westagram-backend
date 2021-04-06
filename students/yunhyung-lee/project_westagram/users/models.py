from django.db import models

class User(models.Model):
    email       = models.CharField(max_length=100)
    password    = models.CharField(max_length=30)
    phone_num   = models.CharField(max_length=30)
    name        = models.CharField(max_length=30)

    class Meta:
        db_table = 'users'
    
