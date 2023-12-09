"""Service functions related to the useraccounts app."""
import os
import string, random
import re
from django.shortcuts import get_object_or_404
from django.http import Http404
from useraccounts.models import User

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
    # modify here: find_username_in_db(sub_name) -> find_username_in_dict(username)
    while find_username_in_db(sub_name):
        count_length = len(str(count))
        if length < 25:
            sub_name = sol_name + str(count)
        else:
            sub_name = sol_name[:length - count_length] + str(count)
        count += 1
    return sub_name

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
    return service_name + suffix if service_name.lower() in APPROVED_AUTH else "None"

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

# def modify_username(username:str) -> str:
#     sol_name = sub_name = username[:30] if len(username) > 30 else username
#     length = len(sub_name)
#     count = 1
#     while find_username_in_db(sub_name) and len(sub_name) < 30:
#         count_length = len(str(count))
#         if length == 30:
#             sub_name = sub_name[:(length - count_length)] + str(count)
#         else:
#             sub_name = sol_name + str(count)
#         count += 1
#     return sub_name