import socket

from .message import Message
from .utils import byte_to_message


class _Client:

    def __init__(self, address, port):
        print("Client: Starting...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.__is_running = True
        self.__commands = {}
        print("Client: Connected.")

    def run(self):
        print("Client: Listening...")
        while self.__is_running:
            try:
                msg = self.socket.recv(8000)
            except ConnectionResetError:
                break

            if msg == b'':
                print("Client: The server closed the connection...")
                break

            for message in byte_to_message(msg):
                if message.name in self.__commands:
                    print("Client:", self.socket.getpeername(), "sent [", message, "]")
                    self.__commands[message.name](self, *message.args)
                else:
                    print("Client WARNING: Unknown command", message.name)

        self.socket.close()
        print("Client: Disconnected.")

    def register_command(self, name, callback):
        self.__commands[name] = callback
        print("Client: Registered command [", name, "]")

    def kill(self):
        self.__is_running = False

    def send(self, message, *args):
        msg = Message(message, *args)
        print("Client: sending [", msg, "] to", self.socket.getpeername())
        msg.send(self.socket)
