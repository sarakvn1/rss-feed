from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_time = models.DateTimeField("Created Time", auto_now_add=True)
    updated_time = models.DateTimeField("Updated Time", auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Source(BaseModel):
    url = models.URLField()
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    last_modified = models.TextField(blank=True, null=True)
    etag = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = [('user', 'url')]


class Feed(BaseModel):
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    content = models.TextField()
    title = models.TextField()
    published_time = models.DateTimeField("Published Time")
    guid = models.TextField(blank=True, null=True, unique=True)
    image = models.URLField(blank=True, null=True)
    url = models.URLField(null=True)


class UserFeed(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    feed = models.ForeignKey(Feed, on_delete=models.PROTECT)
    is_read = models.BooleanField(default=False)
    is_bookmarked = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)

    class Meta:
        unique_together = [('user', 'feed')]


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    feed = models.ForeignKey(Feed, on_delete=models.PROTECT)
    parent = models.ForeignKey('self', on_delete=models.PROTECT)
    message = models.TextField()
