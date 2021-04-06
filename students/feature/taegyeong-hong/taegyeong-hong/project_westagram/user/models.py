from django.db import models

# Create your models here.


class Signup(models.Model):
    name = models.EmailField(max_length=150),
    password = models.CharField(max_length=50)
    class meta:
        db_table = 'signups'

    
