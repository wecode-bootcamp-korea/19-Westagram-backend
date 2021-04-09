from django.db    import models
from users.models import User
from django.utils import timezone

class Posting(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    image      = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)




