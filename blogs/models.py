import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation

from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from general.models import BaseModel


class TagBase(GenericUUIDTaggedItemBase, TaggedItemBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.pk}"


class BlogPost(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images')
    
    tags = TaggableManager(through=TagBase)

    def __str__(self):
        return self.title


class Comment(BaseModel):
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    
    def __str__(self):
        return self.content


class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)

    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_added']