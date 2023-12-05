"""Test module for 'useraccounts' using Django REST framework"""
from rest_framework import status
from rest_framework.test import APITestCase
from useraccounts.models import User
from django.urls import reverse

VALID_USER = {
            "username": "testuserA",
            "email": "testuser@mail.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "False"
        }
MISSING_PASSWORD = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "",
            "oauth_login": "False"
        }
INVALID_PASSWORD = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassworssd",
            "oauth_login": "False"
        }
INVALID_EMAIL = {
            "username": "testuser",
            "email": "testuser@",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "False"
        }
INVALID_USERNAME_SHORT = {
            "username": "tes",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "False"
        }
INVALID_USERNAME_LONG = {
            "username": "testtesttesttesttesttestusernametoolong",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "False"
        }
INVALID_AUTHENTICATION = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "",
            "password_confirm": "",
            "oauth_login": "False",  
        }
VALID_OAUTH_USER = {
            "username": "oauthtestuser",
            "email": "testuser@example.com",
            "password": "",
            "password_confirm": "",
            "oauth_login": "skej932kfnma58shdkelanc2kdp",
            "avatar_url":"www.dradha.co/sourceimg.png"
        }
VALID_OAUTH_USER_2 = {
            "username": "oauthtestusernumber2",
            "email": "testuser2@example.com",
            "password": "",
            "password_confirm": "",
            "oauth_login": "skej932kfnma58shdkelanc2kdp",
            "avatar_url":"www.dradha.co/newimage.png"
        }

class UserAPITest(APITestCase):
    """UserAPITest class for various test cases 

    Methods
    -------
    setup()
        Creates a user for testing.
    test_user_get_api()

    """

    def setUp(self):
        """Set up the test method for creating a user"""
        self.user_data = VALID_USER
        self.user_data_missing_password = MISSING_PASSWORD
        self.user_data_invalid_password = INVALID_PASSWORD
        self.user_data_invalid_email = INVALID_EMAIL
        self.user_data_invalid_username_short = INVALID_USERNAME_SHORT
        self.user_data_invalid_username_long = INVALID_USERNAME_LONG
        self.user_data_invalid_authentication = INVALID_AUTHENTICATION
        self.user_data_valid_oauth_user = VALID_OAUTH_USER
        self.user_data_valid_oauth_user_2 = VALID_OAUTH_USER_2
        
        response = self.client.post(reverse("registeruser"), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response2 = self.client.post(reverse("registeruser"), self.user_data_valid_oauth_user)
        self.assertEqual(response2.data["username"], "oauthtestuser")
        self.assertEqual(response2.data["avatar_url"], "www.dradha.co/sourceimg.png")
        self.assertNotIn("password", response2.data)
        self.assertNotIn("oauth_login", response2.data)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_profile(self):
        """Tests the successful creation of a user."""
        response = self.client.post(reverse("registeruser"), {
            "username": "testabcdeuser",
            "email": "test@email.net",
            "password": "testpassword1",
            "password_confirm": "testpassword1",
            "oauth_login": "False"
        })
        self.assertEqual(response.data["username"], "testabcdeuser")
        self.assertEqual(response.data["email"], "test@email.net")
        self.assertEqual(response.data["avatar_url"], "http://www.dradha.co/profile-images/avatar_osteospermum.jpg")
        self.assertNotIn("password", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_password(self): 
        """Tests the failure of creating a user due to missing the password_confirm field."""
        response = self.client.post(reverse("registeruser"), self.user_data_missing_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_password(self):
        """Tests the failure of creating a user due to non-matching passwords."""
        response = self.client.post(reverse("registeruser"), self.user_data_invalid_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_email(self):
        """Tests the failure of creating a user due to an invalid email address."""
        response = self.client.post(reverse("registeruser"), self.user_data_invalid_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_username(self):
        """Tests the failure of creating a user due to an invalid username."""
        response = self.client.post(reverse("registeruser"), self.user_data_invalid_username_short)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse("registeruser"), self.user_data_invalid_username_long)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_user_from_db(self):
        """Tests the retrieval of the first user from the database."""
        saved_user = User.objects.get(username="testuserA")
        self.assertEqual(saved_user.username, "testuserA")
        self.assertEqual(saved_user.email, "testuser@mail.com")

    def test_create_duplicate_user(self):
        """Tests the creation of a duplicate user in db"""
        response = self.client.post(reverse("registeruser"), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_oauth_user(self):
        """Tests the invalid creation of an invalid oauth user"""
        response = self.client.post(reverse("registeruser"), self.user_data_invalid_authentication)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_oauth_user(self):
        """Tests the creation of a valid oauth user"""
        response = self.client.post(reverse("registeruser"), self.user_data_valid_oauth_user_2)
        self.assertEqual(response.data["avatar_url"], "www.dradha.co/newimage.png")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_oauth_user(self):
        """Tests the creation of a duplicate user in db"""
        response = self.client.post(reverse("registeruser"), self.user_data_valid_oauth_user)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

