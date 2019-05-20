#
# This package handles the networking interactions with the different UIs.
#
# Note. It is forbidden to use the characters '\n' and the ESCAPE_CHARACTER defined in constants.py in requests.
#
from qalogging import verbose
from .server import Server

server = Server(12800, 10)

verbose("Loaded package 'network'")
