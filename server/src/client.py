from network.cli_client import CLIClient
from qalogging import announce, info, warning, set_verbose, verbose

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
    client.register_command('choose', choose)
    client.send('request', sentence)
    client.run()


def choose(client, *args: str):
    verbose('The server is asking:', *args)
    info('\nWhat did you mean?')
    options = [arg.replace('~', ' ').split('|') for arg in args]

    for option in options:
        print(' › ' + option[0] + '\t' + option[1] + '\t' + option[2] + ' (' + option[3] + ')')

    while True:
        user: str = input("Type the number of your choice: ")

        user_i: int = int(user)
        if 0 <= user_i < len(options):
            break

    client.send('choice', str(user))


# noinspection PyUnusedLocal
def ast(client, ast_tree: str):
    info('AST:', ast_tree)


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
            try:
                request_sentence(user)
            except ConnectionRefusedError:
                warning('Server unreachable. Please check that it is running.')

    announce('Stopping')


main()
