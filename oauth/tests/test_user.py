import requests
import logging
from django.http import HttpResponseServerError

GITHUB_URL_USER = 'https://api.github.com/user'

# def user_info_access(auth_token):
#     """ Accesses the user information from the Github server.
    
#     Parameters
#     ----------
#     auth_token : str
#     """
#     try:
#         headers = {"Authorization": f"Bearer {auth_token}"}
#         timeout_seconds = 10
#         response = requests.get(GITHUB_URL_USER, headers=headers, timeout=timeout_seconds)
#         response.raise_for_status()  # Raise HTTPError for bad responses
#         return response.json()
#     except requests.RequestException as e:
#         logging.error(f"Error accessing token: {e}")
#         return HttpResponseServerError

# auth_token=""

# user_info = user_info_access(auth_token)

# print(user_info)

from oauth.services import state_generator
