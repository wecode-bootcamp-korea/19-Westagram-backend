from django.db import models

class User(models.Model):
    user_name   = models.CharField(max_length=20, null=True)
    email       = models.EmailField(max_length=200, unique=True)
    password    = models.CharField(max_length=250)
    phone_num   = models.IntegerField(unique=True, null=True)

    class Meta:
        db_table = 'users'
