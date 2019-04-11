#
# This package handles the networking interactions with the different UIs.
#
# Note. It is forbidden to use the characters '\n' and the ESCAPE_CHARACTER defined in this file in requests.
#
from server import Server

ESCAPE_CHARACTER = b'§'

server = Server(12800, 10)
