from django.db import models

class User(models.Model):
# unique=True 옵션    
    email        = models.CharField(max_length=100)
# 이름 작성
    name         = models.CharField(max_length=100)
    phoneNumber  = models.CharField(max_length=50)
    password     = models.CharField(max_length=300)
# 암호화하면 길어짐?? 아직 암호화는 모르겠음

    class Meta:
        db_table = 'users'
