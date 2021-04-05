from django.db import models

class User(models.Model):
    email    = models.CharField(max_length=300)
    name     = models.CharField(max_length=45)
    nickname = models.CharField(max_length=45)
    password = models.CharField(max_length=300)

    class Meta:
        db_table = 'users'

