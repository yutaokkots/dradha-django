"""A subpackage providing additional fields to the User model."""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, MinLengthValidator


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
    
    username = models.CharField(
        max_length=40, 
        unique=True,
        validators=[MinLengthValidator(4)])
    email = models.EmailField(
        max_length=75, 
        blank=False, 
        validators=[EmailValidator])
    avatar_url = models.URLField(
        max_length=300,
        default="http://www.dradha.co/profile-images/avatar_osteospermum.jpg")
    oauth_login = models.BooleanField(
        default=False)

    def __str__(self):
        """Returns a string representation of the user's username"""
        return str(self.username)

    