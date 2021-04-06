from django.db import models

class User(models.Model):
    
    name  = models.CharField(max_length=20)
    email    = models.CharField(max_length=50)
    password = models.TextField()
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'
