from django.db import models

class Feed(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    text   = models.CharField(max_length=255)
    like   = models.ManyToManyField(
        'users.User', 
        through      = 'FeedLike', 
        related_name = 'like'
    )
    tag        = models.ManyToManyField('Tag', through='FeedTag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'feeds'

class Media(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    url  = models.CharField(max_length=500)

    class Meta:
        db_table = 'media'

class Tag(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'tags'

class FeedTag(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    tag  = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'feed_tags'

class FeedLike(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    class Meta:
        db_table = 'feed_likes'

class Comment(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    like   = models.ManyToManyField(
        'users.User', 
        through='CommentLike', 
        related_name='comment_like'
    )
    feed   = models.ForeignKey(Feed, on_delete=models.CASCADE)
    text   = models.CharField(max_length=300)

    class Meta:
        db_table = 'comments'

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)