from django.db import models

class Accounts(models.Model):

    user_id       = models.CharField(max_length = 50)
    user_pw       = models.CharField(max_length = 100)
    user_name     = models.CharField(max_length = 16)
    user_phone    = models.CharField(max_length = 11)
    user_nickname = models.CharField(max_length = 16, null = True)

    class Meta:
        db_table = "accounts"
            

