"""Service functions related to the useraccounts app."""
import os
import string, random
from django.shortcuts import get_object_or_404
from django.http import Http404
from useraccounts.models import User

SECRET_DRADHA = os.environ.get('SECRET_KEY_DRADHA_FRONTEND_BACKEND')


def verify_origin(origin_key: str) -> bool:
    """Verifies the origin of HTTPS request."""
    return origin_key == SECRET_DRADHA

def find_in_db(username:str) -> bool:
    return User.objects.filter(username=username).exists()

    # try:
    #     get_object_or_404(User, username=username)
    #     return True
    # except Http404:
    #     return False

def modify_username(username:str) -> str:
    pass
    # if len(username) > 25:

    # while not find_in_db(username):
    #     len(username)
    
    "hellobillycaretsnoop"

def oauth_uid_generator(service_name: str) -> str:
    """ Random 20 character unique ID generator for the User model. 
    service_name : str
        Name of service (e.g. "dradha", "github")
    """
    char_length = 9
    num_uid = [random.choice(string.ascii_letters + string.digits) for _ in range(char_length)]
    suffix = "-" + "".join(num_uid)
    if len(service_name) > 10:
        service_name = service_name[0:10]
    return service_name + suffix