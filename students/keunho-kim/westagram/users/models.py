from django.db import models



# Create your models here.
from django.forms import PasswordInput


class User(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=14)



    class Meta:
        db_table = "users"
