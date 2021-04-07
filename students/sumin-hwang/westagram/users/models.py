from django.db import models

class User(models.Model):
    mobile_number = models.CharField(max_length=50, unique=True)
    email         = models.EmailField(max_length=200, unique=True)
    name          = models.CharField(max_length=100)
    nickname      = models.CharField(max_length=100)
    password      = models.CharField(max_length=200)
    create_at     = models.DateTimeField(auto_now_add=True)
    update_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
