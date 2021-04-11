from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=200, unique=True)
    password     = models.CharField(max_length=200)
    name         = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100, unique=True)
    profile_img  = models.CharField(max_length=300, null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Following(models.Model):
    follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')

    class Meta:
        db_table = 'followings'