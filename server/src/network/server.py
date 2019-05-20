import atexit
import socket
from threading import Thread

from qalogging import announce, warning, verbose, info
from .client import Client


#
# This file represents a TCP Server and the actions it can do with its clients. This Server implementation launches
# one thread per client, which ables it to run with multiple clients at the same time.
#


class Server:

    def __init__(self, port: int, max_connections: int = 1):
        """
        Instantiates a new Server object, but doesn't start it.
        :param port: The port the server should listen to
        :param max_connections: The maximum number of simultaneous clients.
        """

        info("Server: Booting up...")
        self.clients = []
        self.commands = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", port))
        self.socket.listen(max_connections)
        self.is_running = True
        info("Server: Connected on port", self.socket.getsockname()[1], "\n")
        atexit.register(self.kill)  # Close the server automatically when the program is killed externally

    def run(self):
        """
        Launches this server. This method will block, and clients will begin to be handled.
        """

        announce("Server: Running")
        while self.is_running:
            try:
                self.socket.settimeout(1)
                client, infos = self.socket.accept()
                Thread(target=self.__connect_to_client, args=[client]).start()
            except (socket.timeout, OSError):
                pass
        warning("Server: The socket was closed, stopped listening.")

    def __connect_to_client(self, client):
        """
        Connects to a client.
        :param client: the client to connect to
        """

        self.clients.append(client)
        Client(self, client)
        self.clients.remove(client)

    def register_command(self, name: str, callback):
        """
        Registers a command that will be used by the server.
        :param name: The name of the command
        :param callback: The code to execute when that command is found.
        """

        self.commands[name] = callback
        verbose("Server: Registered command [", name, "]")

    def kill(self):
        """
        Closes this server and its socket.
        """

        self.socket.close()
        self.is_running = False
        [client.close() for client in self.clients]
        info("Server: Disconnected.")
