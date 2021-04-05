from django.db import models

class User(models.Model):
    
    user_id  = models.CharField(max_length=50)
    email    = models.CharField(max_length=50)
    password = models.TextField()
    phone_number = models.CharField(max_length=11)

    class Meta:
        db_table = 'users'
