from django.contrib.auth.models import BaseUserManager
from useraccounts.services import find_in_db, modify_username, oauth_uid_generator

class CustomUserManager(BaseUserManager):
    def create_user(self, username, oauth_user):
        if find_in_db(username):
            modify_username(username)
        if oauth_user == "None":
            oauth_user = oauth_uid_generator("dradha")