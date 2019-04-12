from message import Message
from utils import byte_to_message


#
# Represents a Client from the Server's point of view.
#

class Client:

    def __init__(self, server, socket):
        self.__socket = socket
        self.__server = server
        self.coords = socket.getpeername()
        print("Server:", self.__socket.getpeername(), "has connected.")
        self.__listen()

    def __listen(self):
        while True:
            try:
                self.__receive_messages()
            except ConnectionResetError:
                break
        self.close(clientside=True)

    def __receive_messages(self):
        # Receive maximum 8000 bytes from the socket
        msg = self.__socket.recv(8000)

        # Nothing was received
        if msg == b'':
            return

        for message in byte_to_message(msg):
            if message.name in self.__server.commands:
                print("Server:", self.coords, ">>>", message)
                self.__server.commands[message.name](self.__server, self, *message.args)
            else:
                print("Server WARNING: Unknown command:", message.name)

    def send(self, command, *args):
        """
        Sends a message to the client.
        :param command: The name of the command to call.
        :param args: The args that are sent to that client.
        """

        msg = Message(command, *args)
        print("Server:", self.coords, "<<<", msg)
        msg.send(self.__socket)

    def close(self, clientside=False):
        """
        Disconnects this client.
        :param clientside: Whether this client disconnected itself, or was disconnected by the server.
        """

        if clientside:
            print("Server:", self.coords, "was disconnected.")
        else:
            print("Server:", self.coords, "was disconnected by the server.")
            self.__socket.close()
