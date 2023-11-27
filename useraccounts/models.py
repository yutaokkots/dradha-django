"""A subpackage providing additional fields to the User model."""
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Class representing an abstraction of the django-auth model, User.
    
    This subpackage defines a custom User model, named User, which extends
    Django's built-in AbstractUser.

    Attributes
    ----------
    username (CharField):
        A field for storing the username.
    email (CharField): 
        A field for storing the email address.
    """
    
    username = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=75, blank=False)

    def __str__(self):
        """Returns a string representation of the user's username"""

        return str(self.username)
