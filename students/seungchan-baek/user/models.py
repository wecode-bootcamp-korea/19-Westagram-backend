from django.db import models

class User(models.Model):
    identification = models.CharField(max_length=50)
    password       = models.CharField(max_length=50)
    name           = models.CharField(max_length=50)
    nickname       = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'
