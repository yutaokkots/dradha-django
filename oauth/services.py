"""Service functions related to the oauth app."""
import random
import string
from django.core.cache import cache
# from useraccounts.services import oauth_login_validator, find_oauthlogin_in_db, username_validator

def set_state(state:str, key_length:int=20, timeout:int=600) -> None:
    """Saves the generated state in the cache with a time-out of 10 minutes (600 seconds).

    For caching in psql database:
    cache.set(key, value, timeout=DEFAULT_TIMEOUT, version=None) 
    # DEFAULT_TIMEOUT is in seconds, an int.
    """
    key_state = state[:key_length]
    cache.set(key_state, state, timeout=timeout)

def state_generator(length:int=20) -> str:
    """Generates a random state of length, 'length:int'. """
    code = [random.choice(string.ascii_letters + string.digits) for _ in range(length)]
    return "".join(code)

def verify_state(state:str, key_length:int=20) -> bool:
    """ Verifies the state in the cache.

    Gets the state by its key (determined by the key_length), 
    and verifies that the cached state is equal to the input state.

    Parameters
    ----------
    state : str
    key_length : int

    Returns
    -------
    bool
    """
    value = cache.get(state[:key_length])    
    return value == state

# def user_model_flow(user_data):
#     """ """
#     # Custom service function to ensure unique username.
#     username = username_validator(user_data["login"])
#     email = user_data["email"]
#     # Custom service function to ensure unique oauth_login (uid).
#     oauth_login = oauth_login_validator("github")      
#     avatar_url = user_data["avatar_url"]

#     user_object = {
#             "username" : username, 
#             "email" : email, 
#             "avatar_url" : avatar_url, 
#             "oauth_login" : oauth_login
#         }
#     set_state(state=oauth_login)

#     pass
""" 
    parses the user information for model
    - check that the username is unique; if not, create new one
    - create a oauth-login field
    - store the oauth_login in the cache, ensure it is unique
    - send the object to the createuser endpoint/deserializer for saving to model
    - take the request back to the oauth/views, and redirect to main page if successfull
    - or redirect to error page if failed


"""


# def oauth_uid_generator(service_name: str) -> str:
#     """ Random 20 character unique ID generator for the User model. 
#     service_name : str
#         Name of service (e.g. "dradha", "github")
#     """
#     char_length = 9
#     num_uid = [random.choice(string.ascii_letters + string.digits) for _ in range(char_length)]
#     suffix = "-" + "".join(num_uid)
#     if len(service_name) > 10:
#         service_name = service_name[0:10]
#     return service_name + suffix