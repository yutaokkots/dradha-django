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
            "oauth_login": "None"
        }
MISSING_PASSWORD = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "",
            "oauth_login": "None"
        }
INVALID_PASSWORD = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassworssd",
            "oauth_login": "None"
        }
INVALID_EMAIL = {
            "username": "testuser",
            "email": "testuser@",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "None"
        }
INVALID_USERNAME_SHORT = {
            "username": "tes",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "None"
        }
INVALID_USERNAME_LONG = {
            "username": "testtesttesttesttesttestusernametoolong",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "oauth_login": "None"
        }
NO_PASSWORD = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "",
            "password_confirm": "",
            "oauth_login": "None",  
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
    """UserAPITest class for various test cases 

    Methods
    -------
    setup()
        Creates two users (a regular user and an oauth user) for initial testing setup.
    test_create_user_profile()
        Creates another valid user profile.
    test_create_missing_password()  
        (Failure) Attempts to create a profile with a missing password. 
    test_create_invalid_password()
        (Failure) Attempts to create a profile with non-matching passwords. 
    test_create_invalid_email()
        (Failure) Attempts to create a profile with an invalid email. 
    test_create_invalid_username()
        (Failure) Attempts to create a profile with a short or long username. 
    test_create_duplicate_user()
        (Failure) Attempts to create duplicate(regular and oauth) users. 
    test_create_no_passwords
        (Failure) Attempts to create a user with no passwords. 
    test_retrieve_users_from_db()
        Retrieves both users from setup(). 
    test_invalid_oauth_user()
        (Failure) Attempts to create an oauth user with incorrect permissions. 


    """

    def setUp(self):
        """Set up the test method for creating a user"""
        self.user_data = VALID_USER
        self.user_data_missing_password = MISSING_PASSWORD
        self.user_data_invalid_password = INVALID_PASSWORD
        self.user_data_invalid_email = INVALID_EMAIL
        self.user_data_invalid_username_short = INVALID_USERNAME_SHORT
        self.user_data_invalid_username_long = INVALID_USERNAME_LONG
        self.user_data_no_password = NO_PASSWORD
        self.user_data_valid_oauth_user = VALID_OAUTH_USER
        self.user_data_valid_oauth_user_2 = VALID_OAUTH_USER_2
        self.user_data_invalid_oauth_user = INVALID_OAUTH_USER 

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
            "oauth_login": "None"
        })
        self.assertEqual(response.data["username"], "testabcdeuser")
        self.assertEqual(response.data["email"], "test@email.net")
        self.assertEqual(response.data["avatar_url"], "http://www.dradha.co/profile-images/avatar_osteospermum.jpg")
        self.assertNotIn("password", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        all_users = User.objects.all()
        self.assertEqual(all_users.count(), 3)
        self.assertNotEqual(all_users.count(), 2)

    def test_create_missing_password(self): 
        """Tests the failure of creating a user due to missing the password_confirm field."""
        response = self.client.post(reverse("registeruser"), self.user_data_missing_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        all_users = User.objects.all()
        self.assertEqual(all_users.count(), 2)
        self.assertNotEqual(all_users.count(), 3)

    def test_create_invalid_password(self):
        """Tests the failure of creating a user due to non-matching passwords."""
        response = self.client.post(reverse("registeruser"), self.user_data_invalid_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        all_users = User.objects.all()
        self.assertEqual(all_users.count(), 2)
        self.assertNotEqual(all_users.count(), 3)

    def test_create_invalid_email(self):
        """Tests the failure of creating a user due to an invalid email address."""
        response = self.client.post(reverse("registeruser"), self.user_data_invalid_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        all_users = User.objects.all()
        self.assertEqual(all_users.count(), 2)
        self.assertNotEqual(all_users.count(), 3)

    def test_create_invalid_username(self):
        """Tests the failure of creating a user due to an invalid username."""
        response_1 = self.client.post(reverse("registeruser"), self.user_data_invalid_username_short)
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response_1.status_code, status.HTTP_201_CREATED)
        response_2 = self.client.post(reverse("registeruser"), self.user_data_invalid_username_long)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response_2.status_code, status.HTTP_201_CREATED)
        all_users = User.objects.all()
        self.assertEqual(all_users.count(), 2)
        self.assertNotEqual(all_users.count(), 4)

    def test_create_duplicate_user(self):
        """Tests the creation of duplicate users in db"""
        response_1 = self.client.post(reverse("registeruser"), self.user_data)
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response_1.status_code, status.HTTP_201_CREATED)
        response_2 = self.client.post(reverse("registeruser"), self.user_data_valid_oauth_user)
        self.assertNotEqual(response_2.status_code, status.HTTP_201_CREATED)
        all_users = User.objects.all()
        self.assertEqual(all_users.count(), 2)
        self.assertNotEqual(all_users.count(), 4)

    def test_create_no_passwords(self):
        """Tests the invalid creation of an invalid oauth user"""
        response = self.client.post(reverse("registeruser"), self.user_data_no_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        all_users = User.objects.all()
        self.assertEqual(all_users.count(), 2)
        self.assertNotEqual(all_users.count(), 3)

    def test_create_oauth_user(self):
        """Tests the creation of a valid oauth user"""
        response = self.client.post(reverse("registeruser"), self.user_data_valid_oauth_user_2)
        self.assertEqual(response.data["avatar_url"], "www.dradha.co/newimage.png")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        all_users = User.objects.all()
        self.assertEqual(all_users.count(), 3)
        self.assertNotEqual(all_users.count(), 2)

    def test_retrieve_users_from_db(self):
        """Tests the retrieval of the first and second users from the database."""
        saved_user_1 = User.objects.get(username="testuserA")
        self.assertEqual(saved_user_1.username, "testuserA")
        self.assertEqual(saved_user_1.email, "testuser@mail.com")
        saved_user_2 = User.objects.get(username="oauthtestuser")
        self.assertEqual(saved_user_2.username, "oauthtestuser")
        self.assertEqual(saved_user_2.email, "testuseroauth@example.com")
        self.assertEqual(saved_user_2.avatar_url, "www.dradha.co/sourceimg.png")

    def test_invalid_oauth_user(self):
        """Tests an oauth user that does not have the right permissions."""
        response = self.client.post(reverse("registeruser"), self.user_data_invalid_oauth_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        all_users = User.objects.all()
        self.assertEqual(all_users.count(), 2)
        self.assertNotEqual(all_users.count(), 3)
