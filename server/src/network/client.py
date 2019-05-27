from qalogging import info, verbose, warning
from .message import Message
from .utils import byte_to_message


#
# Represents a Client from the Server's point of view.
#

class Client:

    def __init__(self, server, socket):
        self.__socket = socket
        self.__server = server
        self.coords = socket.getpeername()
        info("Server:", self.__socket.getpeername(), "has connected.")

    def listen(self):
        while True:
            try:
                self.receive_message()
            except (ConnectionResetError, OSError):
                break
        self.close(clientside=True)

    def receive_message(self):
        # Receive maximum 8000 bytes from the socket
        msg = self.__socket.recv(8000)

        # Nothing was received
        if msg == b'':
            return

        for message in byte_to_message(msg):
            if message.name in self.__server.commands:
                verbose("Server:", self.coords, "sent [", message, "]")
                self.__server.commands[message.name](
                    self.__server, self, *message.args)
            else:
                warning("Server: Unknown command [", message.name, "]")

    def send(self, command, *args):
        """
        Sends a message to the client.
        :param command: The name of the command to call.
        :param args: The args that are sent to that client.
        """

        msg = Message(command, *args)
        verbose("Server: sending [", msg, "] to", self.coords)
        msg.send(self.__socket)

    def close(self, clientside=False):
        """
        Disconnects this client.
        :param clientside: Whether this client disconnected itself, or was disconnected by the server.
        """

        if clientside:
            info("Server:", self.coords, "was disconnected.")
        else:
            info("Server:", self.coords, "was disconnected by the server.")
            self.__socket.close()
