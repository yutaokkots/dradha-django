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
    
    USERNAME_FIELD = "oauth_login"
    
    username = models.CharField(
        max_length=30, 
        unique=True,
        validators=[MinLengthValidator(4)])
    email = models.EmailField(
        max_length=75, 
        blank=True, 
        validators=[EmailValidator])
    oauth_login = models.CharField(
        default="None",
        unique=True,
        max_length=20)
    avatar_url = models.CharField(
        max_length=300,
        blank=True,
        default="http://www.dradha.co/profile-images/avatar_osteospermum.jpg")

    #objects = CustomUserManager()


    def __str__(self):
        """Returns a string representation of the user's username"""
        return str(self.username)

    
    # def create_user(cls, username, email, password, **kwargs):
    #     user = super().create_user(username, email, password)
    #     for field, value in kwargs.items():
    #         setattr(user, field, value)
    #     user.save()
    #     return user
    