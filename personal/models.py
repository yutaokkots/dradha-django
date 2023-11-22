"""A subpackage providing fields for the Bookmark model."""
from django.db import models
from django.contrib.auth.models import User

class Bookmark(models.Model):
    """Class representing a bookmark."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    notes = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SocialLinks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.url
