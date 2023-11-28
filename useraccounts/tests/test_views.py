"""Test module for 'useraccounts' using Django REST framework"""
from rest_framework.test import APITestCase
from useraccounts.models import User
from django.urls import reverse

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
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user.set_password("testpassword")
        self.user.save()

    def test_user_login(self):
        self.client.login(username="testuser", password="testpassword")

    def test_user_get_profile(self):
        """Test method for getting user information"""
        response = self.client.get(reverse("getuser", kwargs={"user_id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.user_data["username"])
        self.assertEqual(response.data["email"], self.user_data["email"])
