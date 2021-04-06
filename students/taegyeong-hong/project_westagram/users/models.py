from django.db import models

# Create your models here.

class User(models.Model):
    email       = models.CharField(max_length=50)
    password    = models.CharField(max_length=50)
    name        = models.CharField(max_length=50)
    phone_num   = models.CharField(max_length=50)

    class meta:
        db_table ='users'
