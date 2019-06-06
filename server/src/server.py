#
# This is the main file of the software.
#
import traceback
from typing import List, Tuple

from conversion.converter import convert
from network.client import Client
from network.server import Server
from qalogging import announce, set_client, set_verbose, verbose, error, warning, info
from time import sleep
from wikidata.ask import set_ask_function
from sparql.queryBuilder.query_builder import QueryBuilder

user_choice = None


def ask_client(options: List[Tuple[str, str, str, str]]) -> str:
    """
    Asks the client to choose between multiple Wikidata objects.
    :param options: A list of quadruplets: (q-code, name, description, URL on Wikidata)
    :return The one the user chose
    """
    if len(options) == 0:
        error("The server just requested to ask a question to the client, but didn't provide any possible answer! "
              "Skipping.")
        verbose("Requested a question without providing an answer")
        traceback.print_stack()
        return ""
    elif len(options) == 1:
        warning(
            'Asking a question with only one possible answer, the client will not be prompted.')
        return options[0][0]

    from network.server import server
    tmp = [str(i) + "|" + "|".join(
        [o.replace('|', '~').replace(' ', '~') for o in options[i][1:4]]
    ) for i in range(len(options))]
    verbose("I'm going to ask the client to choose between [", tmp, "]")

    if len(server.clients) == 0:
        error("No clients are connected at this point.")
        raise Exception("Trying to ask the client, but there's no client.")
    elif len(server.clients) > 1:
        warning("Currently,", len(server.clients),
                "are connected; the first one will be selected.")

    client = server.clients[0]
    verbose("The question will be asked to client [", client, "]")

    client.send("choose", *tmp)

    client.receive_message()
    info('The client chose [', user_choice, ']')
    user = int(user_choice)
    return options[user][0]


def client_choice(server: Server, client: Client, choice: str):
    global user_choice
    user_choice = choice


# noinspection PyUnusedLocal
def request(server: Server, client: Client, request: str):
    from nltk2qo.converter import nltk_to_query_objects
    client.send('debug', 'received')
    set_client(client)
    ast = convert([request])
    client.send('ast', str(ast[0]))
    qo = nltk_to_query_objects(ast)
    for sentence in qo:
        qb = QueryBuilder(sentence)
        qb.build()
    set_client(False)
    client.close()


def main():
    announce('Starting ccg2lambda QA Assistant Server...')
    from network.server import server

    # Here we can register commands if we ever need to
    server.register_command('request', request)
    server.register_command('choice', client_choice)

    # The server starts listening to requests
    try:
        server.run()
    except KeyboardInterrupt:
        print('\nThe user killed the server...')
    # The above method is blocking: the code never reaches this point


set_verbose(True)
set_ask_function(ask_client)
main()
