"""Service functions related to the useraccounts app."""
import os
import string, random
import re
from django.shortcuts import get_object_or_404
from django.http import Http404
from useraccounts.models import User
from oauth.services import set_state

SECRET_DRADHA = os.environ.get('SECRET_KEY_DRADHA_FRONTEND_BACKEND')
APPROVED_AUTH = ["dradha", "github"]

def verify_origin(origin_key: str) -> bool:
    """Verifies the origin of HTTPS request."""
    return origin_key == SECRET_DRADHA

def find_username_in_db(username) -> bool:
    """Returns bool if 'username' exists in database for User model."""
    return User.objects.filter(username=username).exists()
        
def modify_username(username:str) -> str:
    """Modifies the username to meet unique=True and max_length=30 constraints."""
    sol_name = sub_name = username[:30] if len(username) > 30 else username
    length = len(sub_name)
    count = 1
    while find_username_in_db(sub_name):
        count_length = len(str(count))
        if length < 25:
            sub_name = sol_name + str(count)
        else:
            sub_name = sol_name[:length - count_length] + str(count)
        count += 1
    return sub_name

def username_validator(username:str) -> str:
    """This function uses helper functions to return a valid username. 
    It checks to see if the input username is in the db, and if so, creates
    a modfied version of the username. 
    """
    if find_username_in_db(username):
        username = modify_username(username)
    return username

def user_model_flow(user_data):
    """Function to pass user_data and create valid fields prior to serialization.
    Input
    -----
    user_data : dict
        A dictionary containing user data with the following keys:
        - 'login': str - The user's login/username.
        - 'email': str - The user's email address.
        - 'password' : str - The user's password.
        - 'password_confirm' : str - The user's confirmation password.
        - 'oauth_login' : str - User's Auth login type; "Dradha", "Github", or other.
    Returns
    -------
    dict
        A dictionary representing a user object with the following fields:
        - username : str - Validated and unique username.
        - email : str - The user's email address
        - password : str - The user's password.
        - password_confirm : str - The user's confirmation password.
        - oauth_login : str - Validated and unique id (uid) created using the input.
    Notes
    -----
    - The 'login' and 'oauth_login' fields are processed through custom validation functions ('username_validator' and 'oauth_login_validator') to ensure uniqueness and validity.
    - The 'oauth_login' is saved in cache using the 'set_state' function.

    """
    # Custom service function to ensure unique username.
    username = username_validator(user_data["username"])
    email = user_data["email"]
    password = user_data["password"]
    password_confirm = user_data["password_confirm"]
    # Use custom service function to ensure unique 'oauth_login' (uid).
    oauth_type = user_data["oauth_login"]
    oauth_login = oauth_login_validator(oauth_type)      
    user_object = {
            "username" : username, 
            "email" : email, 
            "oauth_login" : oauth_login,
        }
    if password and password_confirm:
        user_object["password"] = password
        user_object["password_confirm"] = password_confirm
    if oauth_type.lower() != "dradha":
        set_state(state=oauth_login)
    return user_object

def oauth_uid_generator(service_name: str) -> str:
    """Random 20 character unique ID generator for the User model. 
    service_name : str
        Name of service (e.g. "dradha", "github")
    """
    char_length = 9
    num_uid = [random.choice(string.ascii_letters + string.digits) for _ in range(char_length)]
    suffix = "-" + "".join(num_uid)
    if len(service_name) > 10:
        service_name = service_name[0:10]
    return service_name.lower() + suffix if service_name.lower() in APPROVED_AUTH else "None"

def oauth_uid_get_service(uid: str) -> str:
    if oauth_uid_check_approved(uid):
        match = re.search(r'(.*)-', uid)
        service = match.group(1)
        return service.lower()
    return ""

def oauth_uid_check_approved(uid:str) -> bool:
    """Returns bool of uid contains allowed auth provider and is a valid uid format.
    valid: 'provider name (up to 10 char)" + "-" + "9-digit id"
    """
    if len(uid) > 20:
        return False
    match_pre = re.search(r'^(.*?)-', uid)
    if not match_pre or uid.count('-') != 1:
        return False
    prov = match_pre.group(1)
    match_suf = re.search(r'-(.*?)$', uid)
    suffix = match_suf.group(1)
    return prov.lower() in APPROVED_AUTH and len(suffix) == 9

def find_oauthlogin_in_db(oauth_login) -> bool:
    """Returns bool if 'oauth_login' exists in database for User model."""
    return User.objects.filter(oauth_login=oauth_login).exists()

def oauth_login_validator(service:str) -> str:
    """This function uses helper functions to return a valid oauth_login. 
    If it receives the name of a valid service, it generates a value for 
    the 'oauth_login', which is a unique id for the user.
    """
    uid = oauth_uid_generator(service)
    # if "uid" == "None": create an exception
    if uid == "None":
        raise Exception
    while find_oauthlogin_in_db(uid) and not oauth_uid_check_approved(uid):
        uid = oauth_uid_generator(service)
    return uid

