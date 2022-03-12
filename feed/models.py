from django.db import models
from django.utils import timezone

from account.models import Account
from group.models import Group

class Feed(models.Model):
    body = models.TextField()
    image = models.ManyToManyField('Image', blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    author_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Account, blank=True, related_name='likes')
    has_url = models.BooleanField(default=False, blank=True)
    url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.author + "-" + self.pk

class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Feed', on_delete=models.CASCADE, related_name="comment_parent")
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Account, blank=True, related_name='comment_likes')

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/post_photos/', blank=True, null=True)

