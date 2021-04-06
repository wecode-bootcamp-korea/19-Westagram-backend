from django.db import models

class User(models.Model):
    email       = models.CharField(max_length=100)
    password    = models.CharField(max_length=20)
    phone_num   = models.CharField(max_length=20, null=True)
    user_name   = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'users'
    
