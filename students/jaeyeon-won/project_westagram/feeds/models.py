from django.db import models
from accounts.models import User

class Feed(models.Model):
    username = models.ForeignKey('accounts.User', on_delete = models.CASCADE)
    contents = models.TextField(max_length=2000)
    title = models.CharField(max_length=100)
    img = models.URLField(max_length=2000,null=True)
    created_at = models.DateTimeField('생성시간', auto_now_add=True)
    modified_at = models.DateTimeField('수정시간', auto_now=True)
    class Meta:
        db_table = 'feed'