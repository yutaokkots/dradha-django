"""Test module for 'useraccounts' using Django REST framework"""
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse

from django.test import TestCase
# Create your tests here.

class UserAPITest(APITestCase):
    """UserAPITest class for various test cases 

    Methods
    -------
    setup()
        Creates a user for testing.
    test_user_get_api()

    """

    def setUp(self):
        """Test method for create a user for testing"""
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_user_get_api(self):
        """Test method for logging in the user"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("userdetail"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data)