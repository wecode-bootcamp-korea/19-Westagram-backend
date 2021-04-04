from django.db import models

class User(models.Model):
    identity       = models.CharField(max_length=45)
    password       = models.CharField(max_length=45)
    name           = models.CharField(max_length=45)
    username       = models.CharField(max_length=45)
    class Meta:
        db_table = 'users'