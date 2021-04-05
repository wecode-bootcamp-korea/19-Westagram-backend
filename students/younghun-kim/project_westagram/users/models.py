from django.db import models
from django.db.models.fields import EmailField

# Create your models here.


class User(models.Model):
    useremail = models.CharField(max_length=128)
    password  = models.CharField(max_length=64)

    class Meta:
        db_table = 'users'


