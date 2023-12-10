"""Test module for 'useraccounts' services: useraccounts.tests.test_services"""
from collections import defaultdict
import django
import re
django.setup()
from django.test import TestCase
from django.db import transaction
from django.db.utils import DataError, IntegrityError
from useraccounts.services import find_username_in_db, modify_username, oauth_uid_check_approved, oauth_uid_generator, find_oauthlogin_in_db
from useraccounts.models import User
from useraccounts.tests.mockusers import mock_users, mock_users_2, mock_users_3
from useraccounts.tests.mockoauthusers import mock_oauth_users

USER_DATA_SET = [
    {"username": "testuser",    "email": "testuser@example.com",    "password": "testpassword", "oauth_login": "dradha-a23bv31"},
    {"username": "newperson123","email": "testuser2@example.com",   "password": "testpassword", "oauth_login": "dradha-v341ab23"},
    {"username": "realuserabc", "email": "testuser3@example.com",   "password": "testpassword", "oauth_login": "dradha-abv12433"}
]

class TestUserServices(TestCase):
    """TestUserServices Class for testing User service functions (from useraccounts.tests.test_services)."""

    @classmethod
    def setUpClass(cls):
        """Method called before any tests are run."""
        super().setUpClass()
        print("\n" + cls.__doc__)

    def setUp(self):
        """Method for setting up test case to create 3 unique users."""
        self.user_data_set = USER_DATA_SET
        user_lst = []
        for user in self.user_data_set:
            user_lst.append(User.objects.create_user(**user))
        self.user_1, self.user_2, self.user_3 = user_lst[0], user_lst[1], user_lst[2]
        self.assertEqual(self.user_1.username, self.user_data_set[0]["username"])
        self.assertEqual(self.user_2.username, self.user_data_set[1]["username"])
        self.assertEqual(self.user_3.username, self.user_data_set[2]["username"])

    def test_user_find_username_in_db(self):
        """Test the 'find_username_in_db(username=)' function in oauth.services."""
        self.assertEqual(find_username_in_db(username="testuser"), True)
        self.assertEqual(find_username_in_db(username="inv"), False)

    def test_modify_username(self):
        """Test the 'modify_username()' function in oauth.services with the db.
        Subtests ensure that:
            (1) user creation will fail if not unique, or length > 30;
            (2) if username does not fit constraints, then a new username 
                    is created for the user; and       
            (3) duplicate username will cause the new username to have 
                    a number appended to the end. 
        """
        with self.subTest("(1) Subtest to ensure username field is less than 30 char."):
            """
            mock_users : List[Dict[str, str]]
                List of mock users with unique 'username' and 'oauth_login' fields.
            all_users_count : int
                Initially records total user count before running subtest.
            """
            all_users_count = User.objects.all().count()
            for i, mock_user in enumerate(mock_users):
                with transaction.atomic():
                    user_name = mock_user["username"]
                    if len(user_name) > 30:
                        with self.assertRaises(DataError):
                            user = User.objects.create_user(**mock_user)
                        #print("(failure): ", user_name)
                    elif find_username_in_db(username=user_name):
                        with self.assertRaises(IntegrityError):
                            user = User.objects.create_user(**mock_user)
                        #print("(failure): ", user_name)
                    else:
                        user = User.objects.create_user(**mock_user)
                        user.save() 
                        all_users_count += 1
                        self.assertEqual(User.objects.all().count(), all_users_count)
                        #print("(success): ", user_name)
                
        with self.subTest("(2) Subtest to ensure modified username is created for the user."):
            """
            mock_users_2 : List[Dict[str, str]]
                List of mock users with the same 'username' as mock_users.
            """
            for i, mock_user_2 in enumerate(mock_users_2):
                user_name = mock_user_2["username"]
                with self.subTest("Tests what happens when character number > 30."):
                    """ mock_users_2[5] has username whose char length is >30. """
                    if len(user_name) > 30:   
                        prev_username = mock_user_2["username"]
                        mock_user_2["username"] = modify_username(user_name)
                        new_username = mock_user_2["username"]
                        self.assertNotEqual(new_username, prev_username , "(failure) Users should not be the same.")
                        self.assertLessEqual(len(new_username), 30, "(failure) len(username) > 30.")
                        self.assertEqual(find_username_in_db(username=new_username), False, "(failure) Users should not be duplicated.")
                with self.subTest("Tests what happens when a duplicate user is present."):
                    """ mock_users_2 that are duplicate and found in the database."""
                    if find_username_in_db(username=user_name):
                        self.assertEqual(find_username_in_db(username=user_name), True)
                        prev_username = mock_user_2["username"]
                        mock_user_2["username"] = modify_username(user_name)
                        new_username = mock_user_2["username"]
                        self.assertEqual(find_username_in_db(username=new_username), False,  "(failure) Users should not be duplicated")
                        self.assertNotEqual(new_username, prev_username, "(failure) Users should not be the same.")
                user = User.objects.create_user(**mock_user_2)
                # print("(success): ", user_name)
        with self.subTest("(3) Subtest to ensure that duplicate username is not created."):
            """
            mock_users_3 : List[Dict[str, str]]
                List of mock users with the same 'username' as mock_users.
            """
            for i, mock_user_3 in enumerate(mock_users_3):
                user_name = mock_user_3["username"]
                if (len(user_name) > 30 or 
                        find_username_in_db(username=user_name)):
                    modified_username = modify_username(user_name)
                    mock_user_3["username"] = modified_username
                    self.assertNotEqual(modified_username, user_name, "(failure) Users should not be the same.")
                user = User.objects.create_user(**mock_user_3)
                user.save()

    def test_valid_oauth_user(self):
        """Tests that the 'oauth-login' field is created effectively and is unique."""
        for mock_oauth_u in mock_oauth_users:
            user_name = mock_oauth_u["username"]
            oauth_login = mock_oauth_u["oauth_login"]
            if find_username_in_db(username=user_name):
                modified_username = modify_username(user_name)
                mock_oauth_u['username'] = modified_username 
            if (not oauth_uid_check_approved(oauth_login) or 
                    not find_oauthlogin_in_db(oauth_login)):
                modified_oauth = oauth_uid_generator("dradha")
                mock_oauth_u["oauth_login"] = modified_oauth
            user = User.objects.create_user(**mock_oauth_u)
            user.save()
        users = User.objects.all()
        for u in users:
            print(f"{u.username} - {u.oauth_login}")
                        