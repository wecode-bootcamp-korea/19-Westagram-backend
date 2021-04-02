from django.db import models

class User(models.Model):
    email = models.CharField(default='', max_length=300, null=False)
    password = models.CharField(default='', max_length=300, null=False)

    class Meta:
        db_table = 'users'

