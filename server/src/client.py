from network.cli_client import CLIClient
from qalogging import announce, info, warning, set_verbose

set_verbose(False)


def request_sentence(sentence: str):
    if '§' in sentence:
        warning('The character § is not allowed in requests, it will be replaced by underscores (_).')
        sentence.replace('§', '_')
    if '\n' in sentence:
        warning('The character EOL (\\n) is not allowed in requests, it will be replaced by dots (.).')
        sentence.replace('\n', '.')

    client = CLIClient("127.0.0.1", 12800)
    client.register_command('debug', debug)
    client.register_command('ast', ast)
    client.register_command('info', server_info)
    client.send('request', sentence)
    client.run()


# noinspection PyUnusedLocal
def ast(client, ast: str):
    info('AST:', ast)


# noinspection PyUnusedLocal
def server_info(client, *args: str):
    info(*args)


# noinspection PyUnusedLocal
def debug(client, msg: str):
    if msg == 'received':
        info('The server has received the request and has started working on it...')
    else:
        warning('Received weird output: command "debug", args:', msg)


def print_help():
    announce('ccg2lambda QA Assistant: Help')
    info(' › q, quit:     \tQuits the software')
    info(' › ?, h, help:  \tDisplays this page')
    info(' › v, verbose:  \tEnables verbose mode')
    # noinspection SpellCheckingInspection
    info(' › nv, noverbose:\tDisables verbose mode')


def main():
    announce("\n Starting...")

    print_help()
    while True:
        user = input("\nSend a request to the server: ")
        # noinspection SpellCheckingInspection
        if user == "quit" or user == "q":
            break
        elif user == "help" or user == "h" or user == "?":
            print_help()
        elif user == "verbose" or user == "v":
            set_verbose(True)
        elif user == "noverbose" or user == "nv":
            set_verbose(False)
        else:
            request_sentence(user)

    announce('Stopping')


main()
