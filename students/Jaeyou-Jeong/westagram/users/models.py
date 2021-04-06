from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=200)
    password     = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    name         = models.CharField(max_length=100)

    class Meta:
        db_table = 'user_info'
