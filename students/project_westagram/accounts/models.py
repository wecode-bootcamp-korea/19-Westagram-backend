from django.db import models

class Accounts(models.Model):

    max_password = 30
    min_password = 8
    max_phone    = 11
    min_phone    = 10
    
    email    = models.CharField(max_length = 50)
    password = models.CharField(max_length = max_password)
    name     = models.CharField(max_length = 16)
    phone    = models.CharField(max_length = max_phone)

    class Meta:
        db_table = "accounts"

