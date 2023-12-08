"""Service functions related to the oauth app."""
import random
import string
from django.core.cache import cache

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