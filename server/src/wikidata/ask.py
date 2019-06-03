# Use this method to ask a question to the client.
#
# This method can be used in the exact same way than 'ask_client' from src/server.py.
# Because of circular dependencies, however, it is not possible to import the real one.
# To fix this problem, the 'ask_client' function in this file provides a link to the real function,
# which is linked automatically by the server code when it starts up.
#

from typing import List, Tuple, Callable
from qalogging import announce, verbose, error, warning, info


def __not_loaded(options: List[Tuple[str, str, str, str]]) -> str:
    error("The 'ask_client' function has not been loaded!")
    warning("Falling back to the first choice provided.")
    return options[0][1]


ask_client: Callable = __not_loaded


def set_ask_function(callback):
    global ask_client
    ask_client = callback
    verbose("Loaded the 'ask' function")
