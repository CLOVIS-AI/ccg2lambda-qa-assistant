from threading import Thread
from unittest import TestCase

# noinspection PyUnusedLocal,PyShadowingNames
from network.server import server


def ping(server, client, msg):
    client.send("pong", msg)


def pong(client, msg):
    TestCase().assertEqual("something", msg)
    client.kill()


# noinspection PyUnusedLocal
def bigger(server, client, first, second, third):
    client.send("smaller", first, second, third)


def smaller(client, first, second, third):
    test = TestCase()
    test.assertEqual("1", first)
    test.assertEqual("2", second)
    test.assertEqual("3", third)
    client.kill()


class TestNetwork(TestCase):

    def test_ping(self):
        server.register_command("ping", ping)
        Thread(target=server.run).start()

        from .cli_client import CLIClient
        client = CLIClient("127.0.0.1", 12800)
        client.register_command("pong", pong)
        client.send("ping", "something")
        client.run()

        server.kill()

    def test_other(self):
        server.register_command("bigger", bigger)
        Thread(target=server.run).start()

        from .cli_client import CLIClient
        client = CLIClient("127.0.0.1", 12800)
        client.register_command("smaller", smaller)
        client.send("bigger", "1", "2", "3")
        client.run()

        server.kill()
