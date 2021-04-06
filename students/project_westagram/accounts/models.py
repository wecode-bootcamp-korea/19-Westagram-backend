from django.db import models

class Accounts(models.Model):
    
    email    = models.CharField(max_length = 50)
    password = models.CharField(max_length = 30)
    name     = models.CharField(max_length = 16)
    phone    = models.CharField(max_length = 11)

    class Meta:
        db_table = "accounts"

