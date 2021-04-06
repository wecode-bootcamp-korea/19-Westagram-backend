from django.db import models
from django.db.models.deletion import CASCADE

from accounts.models import Accounts

class Posts(models.Model):
    
    account     = models.ForeignKey(Accounts, on_delete = CASCADE)
    image_url   = models.CharField(max_length = 255)
    paragraph   = models.CharField(max_length = 255)
    create_time = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        db_table = "posts"
        
class Comments(models.Model):
    
    account = models.ForeignKey(Accounts, on_delete = CASCADE)
    