from .constants import ESCAPE_CHARACTER


class Message:

    def __init__(self, name, *args):
        """
        Instantiates a new Message.
        :param name: The name of the command.
        :param args: The parameters of the command.
        """

        self.name = name
        self.args = []
        for arg in args:
            self.args.append(arg)

    def __str__(self) -> str:
        """
        Converts this object to a String object.
        :return: This object as a String.
        """

        s = self.name
        for arg in self.args:
            s += ' '
            s += str(arg)
        return s

    def send(self, socket):
        """
        Encodes this object and sends it in a Socket.
        :param socket: The socket in which to send this Message.
        """

        s = self.name.encode()
        for arg in self.args:
            s += ESCAPE_CHARACTER + arg.encode()
        s += b"\n"
        try:
            print("Internal: Sending [", s.decode().replace('\n', ''), "]")
            socket.send(s)
        except OSError:
            print("Warning: Cannot send message, invalid connection.")
