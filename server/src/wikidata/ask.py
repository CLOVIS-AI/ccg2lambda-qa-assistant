# Use this method to ask a question to the client.

from typing import List, Tuple
from qalogging import announce, verbose, error, warning, info

__function = None

def ask_client(options: List[Tuple[str, str, str, str]]) -> str:
    if __function is not None:
        verbose("Calling the 'ask' function...")
        return __function(options)
    else:
        error("The 'ask_client' function has not been loaded!")
        raise Exception("Trying to ask the client, but the function hasn't been loaded!")

def set_ask_function(callback):
    global __function
    __function = callback
    verbose("Loaded the 'ask' function")
