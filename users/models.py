"""A subpackage providing fields for the Profile model."""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Class representing a profile."""
    # Each user has a one-to-one relationship with a Django User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=40)
    email = models.CharField(max_length=75, blank=True)
    location = models.CharField(max_length=75, blank=True)
    bio = models.CharField(max_length=200, blank=True)
    # workexp = models.CharField(max_length=200, blank=True)
    # sociallinks = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.username)
