"""Test module for 'useraccounts' using Django REST framework"""
from rest_framework import status
from rest_framework.test import APITestCase
from useraccounts.models import User
from profile.models import Profile
from django.urls import reverse

VALID_USER = {
            "username": "testuserA",
            "email": "testuser@mail.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "Dradha"
        }
MISSING_PASSWORD = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "",
            "oauth_login": "Dradha"
        }
INVALID_PASSWORD = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassworssd",
            "oauth_login": "Dradha"
        }
INVALID_EMAIL = {
            "username": "testuser",
            "email": "testuser@",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "Dradha"
        }
INVALID_USERNAME_SHORT = {
            "username": "tes",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "Dradha"
        }
INVALID_USERNAME_LONG = {
            "username": "testtesttesttesttesttestusernametoolong",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "Dradha"
        }
NO_PASSWORD = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "",
            "password_confirm": "",
            "oauth_login": "Dradha",  
        }
VALID_OAUTH_USER = {
            "username": "oauthtestuser",
            "email": "testuseroauth@example.com",
            "password": "",
            "password_confirm": "",
            "oauth_login": "skej932kfnma58shdkel",
            "avatar_url":"www.dradha.co/sourceimg.png"
        }
VALID_OAUTH_USER_2 = {
            "username": "oauthtestusernumber2",
            "email": "testuser2@example.com",
            "password": "",
            "password_confirm": "",
            "oauth_login": "skej932kfnma58shdkel",
            "avatar_url":"www.dradha.co/newimage.png"
        }
INVALID_OAUTH_USER = {
            "username": "fakeoauthuser",
            "email": "fakeuser@example.com",
            "password": "",
            "password_confirm": "",
            "oauth_login": "nma58sskej932kf",  
        }

class UserAPITest(APITestCase):
    """UserAPITest Class for testing the User views (from useraccounts.tests.testviews).
    
    """
    @classmethod
    def setUpClass(cls):
        """Method called before any tests are run."""
        super().setUpClass()
        doc_str = cls.__doc__.splitlines()
        print("\n" + doc_str[0] if doc_str[0] else "")

    def setUp(self):
        """Set up the test method for creating a user"""
        self.register_url = reverse("registeruser")
        self.valid_user = {
            "username": "testuserA",
            "email": "testuser@mail.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "Dradha"
        }
        self.user_data_valid_oauth_user = {
            "username": "oauthtestuser",
            "email": "testuseroauth@example.com",
            "password": "",
            "password_confirm": "",
            "oauth_login": "Github",
            "avatar_url":"www.dradha.co/sourceimg.png"
        }

        response1 = self.client.post(reverse("registeruser"), self.user_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)

        response2 = self.client.post(reverse("registeruser"), self.user_data_valid_oauth_user)
        self.assertEqual(response2.data["username"], "oauthtestuser")
        self.assertEqual(response2.data["avatar_url"], "www.dradha.co/sourceimg.png")
        self.assertNotIn("password", response2.data)
        self.assertNotIn("oauth_login", response2.data)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

