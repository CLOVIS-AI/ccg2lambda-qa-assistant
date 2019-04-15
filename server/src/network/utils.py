from typing import List

from .constants import ESCAPE_CHARACTER
from .message import Message


def byte_to_message(contents) -> List[Message]:
    """
    Converts bytes received in the socket, into Message objects.
    :param contents: the bytes received by the server
    :return: A list of the messages that were received, after parsing. May be empty if there were no messages.
    """

    messages = []
    if contents != b'':
        for command in contents.split(b'\n'):
            if command != b'':
                print("Internal: Received [", command.decode(), "]")
                parts = command.split(ESCAPE_CHARACTER)
                name = parts[0].decode()
                params = [parts[i].decode() for i in range(1, len(parts))]

                messages.append(Message(name, *params))
    return messages
