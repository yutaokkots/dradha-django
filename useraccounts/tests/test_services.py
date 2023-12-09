"""Test module for 'useraccounts' services: useraccounts.tests.test_services"""
import django
django.setup()
from django.test import TestCase
from django.db import transaction
from django.db.utils import DataError
from useraccounts.services import find_in_db, find_in_db_2,modify_username
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

    def test_user_find_in_db(self):
        """Test the 'find_in_db()' function in oauth.services."""
        self.assertEqual(find_in_db("testuser"), True)
        self.assertEqual(find_in_db("inv"), False)

    def test_modify_username(self):
        """Test the 'modify_username()' function in oauth.services.  
        Ensures that 
            (1) username field is unique and fits Model constraints, and
            (2) if username does not fit constraints,
                then a new username is created for the user.         
        """
        with self.subTest("Subtest to ensure username field is less than 30 char."):
            all_users_count = User.objects.all().count()
            for i, mock_user in enumerate(mock_users):
                with transaction.atomic():
                    if len(mock_user["username"]) > 30:
                        with self.assertRaises(DataError):
                            user = User.objects.create_user(**mock_user)
                        print("(failure): ", mock_user["username"])
                    else:
                        user = User.objects.create_user(**mock_user)
                        user.save() 
                        all_users_count += 1
                        self.assertEqual(User.objects.all().count(), all_users_count)
                        print("(success): ", mock_user["username"])
                
        with self.subTest("Subtest to ensure modified username is created for the user."):
            for i, mock_user_2 in enumerate(mock_users_2):
                with self.subTest("Tests what happens when character number > 30."):
                    if len(mock_user_2["username"]) > 30:   
                        prev_username = modify_username(mock_user_2["username"])
                        mock_user_2["username"] = modify_username(mock_user_2["username"])
                        self.assertNotEqual(mock_user_2["username"], mock_user["username"], "(failure) users are the same.")
                        self.assertLessEqual(len(mock_user_2["username"]), 30, "(failure) len(username) > 30.")
                        self.assertEqual(find_in_db(prev_username), 0, "(failure) A duplicate username was found.")
                with self.subTest("Tests what happens when a duplicate user is present."):
                    if find_in_db(mock_user_2["username"]):
                        self.assertEqual(find_in_db(mock_user_2["username"]), True)
                        mock_user_2["username"] = modify_username(mock_user_2["username"])
                        self.assertEqual(find_in_db(mock_user_2["username"]), False,  "(failure) A duplicate username was found.")
                        self.assertNotEqual(mock_user_2["username"], mock_user["username"])
                    user = User.objects.create_user(**mock_user_2)
                print("(success): ", mock_user_2["username"])
        with self.subTest("Subtest to ensure that duplicate username is not created."):
            for i, mock_user_3 in enumerate(mock_users_3):
                if (len(mock_user_3["username"]) > 30 or 
                        find_in_db(mock_user_3["username"])):
                    mock_user_3["username"] = modify_username(mock_user_3["username"])
                user = User.objects.create_user(**mock_user_3)
                print("(success): ", mock_user_3["username"])
      

       # user = User.objects.create_user(mock_users[0])
        #modify_username()


    def test_modify_oauth_login(self):
        """Tests that the 'oauth-login' field is created effectively and is unique."""
        for mock_oauth_u in mock_oauth_users:
            if find_in_db_2(username=mock_oauth_u["username"]):
                mock_oauth_u['username'] = modify_username[mock_oauth_u["username"]]
            
        pass



    def test_usercreation(self):

        pass
        


