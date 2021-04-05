from django.db    import models
from django.utils import timezone

from datetime     import datetime
from users.models import User

class Posting(models.Model):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_at   = models.DateTimeField(auto_now=True)
    image_url   = models.CharField(max_length=100)
    class Meta:
        db_table='Postings'
