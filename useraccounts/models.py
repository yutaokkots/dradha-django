"""
A subpackage providing fields for the User model.

This subpackage defines a custom User model, named User, which extends
Django's built-in AbstractUser.

Attributes:
    username (CharField): A field for storing the username.
    email (CharField): A field for storing the email address.

Methods:
    __str__(): Returns a string representation of the user's username.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=75, blank=False)

    def __str__(self):
        return self.username
