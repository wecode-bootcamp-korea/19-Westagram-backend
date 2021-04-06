from django.db import models

class User(models.Model):
    name     = models.CharField(max_length=45)
    email    = models.EmailField(max_length=200)
    password = models.CharField(max_length=500)
    phone    = models.CharField(max_length=45)

    class Meta:
        db_table = 'users'

