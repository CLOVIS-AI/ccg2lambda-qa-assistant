import socket

from qalogging import verbose, warning
from .message import Message
from .utils import byte_to_message


class CLIClient:

    def __init__(self, address: str, port: int):
        """
        Initializes a Client. It will connect to the given server, but will not send anything yet.
        :param address: The IP address of the server to connect to
        :param port: The port the server is listening on
        """
        verbose("Client: Starting...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.__is_running = True
        self.__commands = {}
        verbose("Client: Connected.")

    def run(self):
        """
        Starts a loop in which the client will listen to the server. This loops stops when the server or the client
        disconnects.
        """
        verbose("Client: Listening...")
        while self.__is_running:
            try:
                msg = self.socket.recv(8000)
            except ConnectionResetError:
                break

            if msg == b'':
                verbose("Client: The server closed the connection...")
                break

            for message in byte_to_message(msg):
                if message.name in self.__commands:
                    verbose("Client:", self.socket.getpeername(), "sent [", message, "]")
                    self.__commands[message.name](self, *message.args)
                else:
                    warning("Client: Unknown command", message.name)

        self.socket.close()
        verbose("Client: Disconnected.")

    def register_command(self, name: str, callback):
        """
        Registers a command, that can be called by the server.
        :param name: The name of the command.
        :param callback: A function that will be ran whenever the server invokes this command. Its first parameter
        should be the this client object, and any other parameters will be treated as varargs.
        """
        self.__commands[name] = callback
        verbose("Client: Registered command [", name, "]")

    def kill(self):
        """
        Closes this client.
        """
        self.__is_running = False

    def send(self, message, *args):
        """
        Sends a message to the server.
        :param message: The name of the command.
        :param args:
        """
        msg = Message(message, *args)
        verbose("Client: sending [", msg, "] to", self.socket.getpeername())
        msg.send(self.socket)
