""" Mocking the github user information request API."""

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch

# class Token