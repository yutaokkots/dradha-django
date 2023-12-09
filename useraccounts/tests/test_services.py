"""Test module for 'useraccounts' services: useraccounts.tests.test_services"""
from collections import defaultdict
import django
django.setup()
from django.test import TestCase
from django.db import transaction
from django.db.utils import DataError, IntegrityError
from useraccounts.services import find_oauthlogin_in_db, find_username_in_db, modify_username
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

    def test_user_find_username_in_db(self):
        """Test the 'find_username_in_db(username=)' function in oauth.services."""
        self.assertEqual(find_username_in_db(username="testuser"), True)
        self.assertEqual(find_username_in_db(username="inv"), False)

    def test_modify_username_function(self):
        """Test the 'modify_username()' function in oauth.services."""
        def find_username_in_dict(username):
            return username in dictionary.keys()
        
        def modify_username(username:str) -> str:
            sol_name = sub_name = username[:30] if len(username) > 30 else username
            length = len(sub_name)
            count = 1
            # modify here: find_username_in_db(sub_name) -> find_username_in_dict(username)
            while find_username_in_dict(sub_name):
                count_length = len(str(count))

                if length < 25:
                    sub_name = sol_name + str(count)
                else:
                    print(length - count_length)
                    sub_name = sol_name[:length - count_length] + str(count)
                count += 1
                print(sub_name)
            return sub_name
    
        dictionary = defaultdict(int)
        dictionary2 = defaultdict(int)
        usernames_1 = ["bardo", "bardo", "bardo", "bardo", "bardo", "bardo", "bardo"]
        usernames_2 = ["rounded_bardouser_winter_carousel", "rounded_bardouser_winter_carousel",  
                       "rounded_bardouser_winter_carousel", "rounded_bardouser_winter_carousel",  
                       "rounded_bardouser_winter_carousel", "rounded_bardouser_winter_carousel",  
                       "rounded_bardouser_winter_carousel", "rounded_bardouser_winter_carousel",
                       "rounded_bardouser_winter_carousel", "rounded_bardouser_winter_carousel",
                       "rounded_bardouser_winter_carousel", "rounded_bardouser_winter_carousel"]
        
        for u in usernames_1:
            if u in dictionary.keys() or len(u) > 30:
                u = modify_username(u)
            dictionary[u] += 1
        print(dictionary)
        self.assertEqual(len(dictionary.keys()), len(usernames_1))
        for u in usernames_1:
            if u in dictionary.keys() or len(u) > 30:
                u = modify_username(u)
            dictionary[u] += 1
        print(dictionary)

        for u in usernames_2:
            if u in dictionary2.keys() or len(u) > 30:
                print(u)
                u = modify_username(u)
                print(u)

            dictionary2[u] += 1
        print(dictionary2)
  
        for u in usernames_2:
            if u in dictionary2.keys() or len(u) > 30:
                u = modify_username(u)
            dictionary2[u] += 1
        print(dictionary2)
  




    # def test_modify_username(self):
    #     """Test the 'modify_username()' function in oauth.services with the db.
    #     Subtests ensure that:
    #         (1) user creation will fail if not unique, or length > 30;
    #         (2) if username does not fit constraints, then a new username 
    #                 is created for the user and will be created; and       
    #         (3) repeated usernames will cause the new username to have 
    #                 a number appended to the end. 
    #     """
    #     with self.subTest("(1) Subtest to ensure username field is less than 30 char."):
    #         """
    #         mock_users : List[Dict[str, str]]
    #             List of mock users with unique 'username' and 'oauth_login' fields.
    #         all_users_count : int
    #             Initially records total user count before running subtest.
    #         """
    #         all_users_count = User.objects.all().count()
    #         for i, mock_user in enumerate(mock_users):
    #             with transaction.atomic():
    #                 user_name = mock_user["username"]
    #                 if len(user_name) > 30:
    #                     with self.assertRaises(DataError):
    #                         user = User.objects.create_user(**mock_user)
    #                     #print("(failure): ", user_name)
    #                 elif find_username_in_db(username=user_name):
    #                     with self.assertRaises(IntegrityError):
    #                         user = User.objects.create_user(**mock_user)
    #                     #print("(failure): ", user_name)
    #                 else:
    #                     user = User.objects.create_user(**mock_user)
    #                     user.save() 
    #                     all_users_count += 1
    #                     self.assertEqual(User.objects.all().count(), all_users_count)
    #                     #print("(success): ", user_name)
                
    #     with self.subTest("(2) Subtest to ensure modified username is created for the user."):
    #         """
    #         mock_users_2 : List[Dict[str, str]]
    #             List of mock users with the same 'username' as mock_users.
    #         """
    #         for i, mock_user_2 in enumerate(mock_users_2):
    #             user_name = mock_user_2["username"]
    #             with self.subTest("Tests what happens when character number > 30."):
    #                 """ mock_users_2[5] has username whose char length is >30. """
    #                 if len(user_name) > 30:   
    #                     prev_username = mock_user_2["username"]
    #                     mock_user_2["username"] = modify_username(user_name)
    #                     new_username = mock_user_2["username"]
    #                     self.assertNotEqual(new_username, prev_username , "(failure) Users should not be the same.")
    #                     self.assertLessEqual(len(user_name), 30, "(failure) len(username) > 30.")
    #                     self.assertEqual(find_username_in_db(username=new_username), False, "(failure) Users should not be duplicated.")
    #             with self.subTest("Tests what happens when a duplicate user is present."):
    #                 """ mock_users_2 that are duplicate and found in the database."""
    #                 if find_username_in_db(username=user_name):
    #                     self.assertEqual(find_username_in_db(username=user_name), True)
    #                     prev_username = mock_user_2["username"]
    #                     mock_user_2["username"] = modify_username(user_name)
    #                     new_username = mock_user_2["username"]
    #                     self.assertEqual(find_username_in_db(username=new_username), False,  "(failure) Users should not be duplicated")
    #                     self.assertNotEqual(new_username, prev_username, "(failure) Users should not be the same.")
    #             user = User.objects.create_user(**mock_user_2)
    #             print("(success): ", user_name)
    #     with self.subTest("(3) Subtest to ensure that duplicate username is not created."):
    #         """
    #         mock_users_3 : List[Dict[str, str]]
    #             List of mock users with the same 'username' as mock_users.
    #         """
    #         for i, mock_user_3 in enumerate(mock_users_3):
    #             user_name = mock_user_3["username"]
    #             if (len(user_name) > 30 or 
    #                     find_username_in_db(username=user_name)):
    #                 mock_user_3["username"] = modify_username(user_name)
    #             user = User.objects.create_user(**mock_user_3)
    #             print("(success): ", user_name)


    # def test_modify_oauth_login(self):
    #     """Tests that the 'oauth-login' field is created effectively and is unique."""
    #     for mock_oauth_u in mock_oauth_users:
    #         user_name = mock_oauth_u["username"]
    #         if find_username_in_db(username=user_name):
    #             mock_oauth_u['username'] = modify_username(user_name)
            
    #     pass







    def test_usercreation(self):

        pass
        

