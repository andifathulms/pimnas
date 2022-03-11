import string
import random

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from django_editorjs import EditorJsField

from account.models import Account
from group.models import Group

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = EditorJsField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.title)
        super(Post, self).save(*args, **kwargs)
