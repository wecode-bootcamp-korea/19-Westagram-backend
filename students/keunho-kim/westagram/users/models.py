from django.db import models
from django    import forms


# Create your models here.
from django.forms import PasswordInput


class User(models.Model):
    id = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, required=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "users"
