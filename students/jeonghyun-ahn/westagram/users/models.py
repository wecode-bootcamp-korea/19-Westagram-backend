from django.db import models

class Email(models.Model):
    email       = models.CharField(max_length=100)
    password    = models.CharField(max_length=20)
    
    
    class Meta:

        db_table ='emails'

