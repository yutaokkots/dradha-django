"""Service functions related to the useraccounts app."""
import os

SECRET_DRADHA = os.environ['SECRET_KEY_DRADHA_FRONTEND_BACKEND']


def verify_origin(origin_key):
    """Verifies the origin of HTTPS request."""
    return origin_key == SECRET_DRADHA

