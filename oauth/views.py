from django.shortcuts import render
from rest_framework import status, request
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
import requests
import logging
import os
import urllib.parse
import random
import string
import json
from datetime import datetime

# test that I receive something at the callback route
# code
# state (user provided)

GITHUB_URL = 'https://github.com/login/oauth/access_token' # os.environ['SECRET_GITHUB_TOKEN_URL'] #


class GithubStateGenerator(APIView):
    def get(self, request, *args, **kwargs):
        try:
            length = 20
            rand_state = self.state_generator(length)
            ts = self.timestamp()
            response = {
                "state":rand_state,
                "timestamp":ts,
            }
            print(response)
            return Response(data=response, status=status.HTTP_201_CREATED)
        except ValueError as value_error:
            error_message = f"ValueError: {value_error}"
            return Response(data={"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

    def state_generator(self, length:int) -> str:
        code = [random.choice(string.ascii_letters + string.digits) for _ in range(length)]
        return "".join(code)
    
    def timestamp(self):
        return json.dumps(datetime.now().isoformat())


class GithubOauthAPI(APIView):
    """ Class for the callback route once user submits login information 
    for Github OAuth2 authenticaion. 
    """
    
    def get(self, request, *args, **kwargs):
        print(request.query_params)
        return redirect('http://localhost:3000')

    def post(self, request, *args, **kwargs):
        try:
            self.code = request.data["code"]
        except KeyError as e:
            return Response({"error": f"Missing {e} parameter"}, status=status.HTTP_400_BAD_REQUEST)
        urlparams = self.post_github()
        #
        self.access_token_url = f"{GITHUB_URL}?{urlparams}"
        print(self.access_token_url)
        #logging.info(self.access_token_url)
        print(self.token_access())
        return Response({}, status=status.HTTP_201_CREATED)
    
    def post_github(self):
        parameters = {
            "client_id": os.environ['SECRET_ID_GITHUB'], 
            "client_secret": os.environ['SECRET_KEY_GITHUB'], 
            "code": self.code, 
            "redirect_uri": "/auth/tokengithub"

        }
        return urllib.parse.urlencode(parameters)

    def token_access(self):
        try:
            headers = {"Accept": "application/json"}
            response = requests.post(self.access_token_url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
            print(response.json())
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error accessing token: {e}")
            return None

    def post_token(self,request, *args, **kwargs):
        print(request)
        print(request.data)
