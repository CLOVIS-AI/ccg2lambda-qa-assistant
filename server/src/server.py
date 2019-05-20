#
# This is the main file of the software.
#
from conversion.converter import convert
from network.client import Client
from network.server import Server
from qalogging import announce, set_client, set_verbose

set_verbose(True)


# noinspection PyUnusedLocal
def request(server: Server, client: Client, request: str):
    client.send('debug', 'received')
    set_client(client)
    ast = convert([request])
    client.send('ast', str(ast[0]))
    set_client(False)
    client.close()


def main():
    announce('Starting ccg2lambda QA Assistant Server...')
    from network.server import server

    # Here we can register commands if we ever need to
    server.register_command('request', request)

    # The server starts listening to requests
    try:
        server.run()
    except KeyboardInterrupt:
        print('\nThe user killed the server...')
    # The above method is blocking: the code never reaches this point


main()
