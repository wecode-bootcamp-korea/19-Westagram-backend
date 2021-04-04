from django.db import models

class User(models.Model):
    mobile_number = models.IntegerField(unique=True, null=True)
    email         = models.EmailField(max_length=200, unique=True, null=True)
    name          = models.CharField(max_length=100)
    user_name     = models.CharField(max_length=100, unique=True)
    password      = models.CharField(max_length=200)
    create_at     = models.DateTimeField(auto_now_add=True)
    update_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
