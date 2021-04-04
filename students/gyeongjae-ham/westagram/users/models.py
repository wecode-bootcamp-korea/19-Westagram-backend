from django.db import models
from django import forms

from phone_field import PhoneField

class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=45)
    number = PhoneField()

    class Meta:
        db_table = 'users'

