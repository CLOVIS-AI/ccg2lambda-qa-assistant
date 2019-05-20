import socket

from qalogging import verbose, warning
from .message import Message
from .utils import byte_to_message


class CLIClient:

    def __init__(self, address, port):
        verbose("Client: Starting...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.__is_running = True
        self.__commands = {}
        verbose("Client: Connected.")

    def run(self):
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

    def register_command(self, name, callback):
        self.__commands[name] = callback
        verbose("Client: Registered command [", name, "]")

    def kill(self):
        self.__is_running = False

    def send(self, message, *args):
        msg = Message(message, *args)
        verbose("Client: sending [", msg, "] to", self.socket.getpeername())
        msg.send(self.socket)
