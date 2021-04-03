from django.db import models

class User(models.Model):
    email    = models.CharField(default='', max_length=300, null=False)
    name     = models.CharField(default='', max_length=45, null=False)
    nickname = models.CharField(default='', max_length=45, null=False)
    password = models.CharField(default='', max_length=300, null=False)

    class Meta:
        db_table = 'users'

