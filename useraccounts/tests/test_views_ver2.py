"""Test module for 'useraccounts' using Django REST framework"""
import re
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from useraccounts.models import User
from useraccounts.services import oauth_login_validator, username_validator, user_model_flow
from profile.models import Profile

VALID_USER = {
            "username": "testuserA",
            "email": "testuser@mail.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "Dradha"
        }
# MISSING_PASSWORD = {
#             "username": "testuser",
#             "email": "testuser@example.com",
#             "password": "testpassword",
#             "password_confirm": "",
#             "oauth_login": "Dradha"
#         }
# INVALID_PASSWORD = {
#             "username": "testuser",
#             "email": "testuser@example.com",
#             "password": "testpassword",
#             "password_confirm": "testpassworssd",
#             "oauth_login": "Dradha"
#         }
# INVALID_EMAIL = {
#             "username": "testuser",
#             "email": "testuser@",
#             "password": "testpassword",
#             "password_confirm": "testpassword",
#             "oauth_login": "Dradha"
#         }
# INVALID_USERNAME_SHORT = {
#             "username": "tes",
#             "email": "testuser@example.com",
#             "password": "testpassword",
#             "password_confirm": "testpassword",
#             "oauth_login": "Dradha"
#         }
# INVALID_USERNAME_LONG = {
#             "username": "testtesttesttesttesttestusernametoolong",
#             "email": "testuser@example.com",
#             "password": "testpassword",
#             "password_confirm": "testpassword",
#             "oauth_login": "Dradha"
#         }
# NO_PASSWORD = {
#             "username": "testuser",
#             "email": "testuser@example.com",
#             "password": "",
#             "password_confirm": "",
#             "oauth_login": "Dradha",  
#         }
# VALID_OAUTH_USER = {
#             "username": "oauthtestuser",
#             "email": "testuseroauth@example.com",
#             "password": "",
#             "password_confirm": "",
#             "oauth_login": "skej932kfnma58shdkel",
#             "avatar_url":"www.dradha.co/sourceimg.png"
#         }
# VALID_OAUTH_USER_2 = {
#             "username": "oauthtestusernumber2",
#             "email": "testuser2@example.com",
#             "password": "",
#             "password_confirm": "",
#             "oauth_login": "skej932kfnma58shdkel",
#             "avatar_url":"www.dradha.co/newimage.png"
#         }
# INVALID_OAUTH_USER = {
#             "username": "fakeoauthuser",
#             "email": "fakeuser@example.com",
#             "password": "",
#             "password_confirm": "",
#             "oauth_login": "nma58sskej932kf",  
#         }

class UserAPITest(APITestCase):
    """UserAPITest Class for testing the User views (from useraccounts.tests.testviews)."""

    @classmethod
    def setUpClass(cls):
        """Method called before any tests are run."""
        super().setUpClass()
        doc_str = cls.__doc__.splitlines()
        print("\n" + doc_str[0] if doc_str[0] else "")

    def setUp(self):
        """Set up the test method for creating a user.
        Perform a post-request using valid user info (for a normal registration process).
        """
        self.register_url = reverse("registeruser")
        self.oauth_url = reverse("callback")
        self.valid_user = {
            "username": "userabc",
            "email": "testuser@mail.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "Dradha"
        }
        response1 = self.client.post(self.register_url, self.valid_user)
        self.assertEqual(response1.data['username'], "userabc")
        u = User.objects.get(username="userabc")
        user_oauth_login = u.oauth_login
        self.assertGreater(len(user_oauth_login), 10)
        self.assertLessEqual(len(user_oauth_login), 20)
        match = re.search(r'-(.*)', user_oauth_login)
        code = match.group(1)
        self.assertEqual(len(code), 9)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        print("UserAPITest.setUp() (success).")

    def test_oauth_user_flow(self) -> None:
        """Perform a post-request using valid user info (for an oauth registration process)."""
        test_user = {
            "username": "oauthuserabc",
            "email": "testuseroauth@example.com",
            "oauth_login": "Github",
            "password": "",
            "password_confirm": "",
            "avatar_url":"www.dradha.co/sourceimg.png"
        }
        response2 = self.client.post(self.register_url, test_user)
        self.assertEqual(response2.data['username'], "oauthuserabc")
        self.assertEqual(response2.data["avatar_url"], "www.dradha.co/sourceimg.png")
        self.assertNotIn("password", response2.data)
        self.assertNotIn("oauth_login", response2.data)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        print("UserAPITest.test_oauth_user_flow() (success).")

        
    # def test_username_validator(self):
    #     """Tests the 'username_validator()' function in useraccounts.services."""
    #     test_username_1 = "userabc"
    #     u1 = username_validator(test_username_1)
    #     self.assertEqual(u1, "userabc1")

    # def test_user_model_flow(self):
    #     """Tests the 'user_model_flow()' function in useraccounts.services."""
    #     test_user = {
    #         "username": "usercdef",
    #         "email": "usercdef@mail.com",
    #         "password": "potluck123",
    #         "password_confirm": "potluck123",
    #         "oauth_login": "Dradha"
    #     }
    #     modified_user = user_model_flow(test_user)
    #     self.assertEqual(modified_user["username"], "usercdef")
    #     self.assertEqual(modified_user["email"], "usercdef@mail.com")
    #     self.assertEqual(modified_user["password"], "potluck123")
    #     self.assertEqual(modified_user["password_confirm"], "potluck123")
    #     user_oauth_login = modified_user["oauth_login"]
    #     self.assertGreater(len(user_oauth_login), 10)
    #     self.assertLessEqual(len(user_oauth_login), 20)
    #     match = re.search(r'-(.*)', user_oauth_login) 
    #     code = match.group(1)
    #     self.assertEqual(len(code), 9)
    #     u = User.objects.all()
    #     for user in u:
    #         print(user)