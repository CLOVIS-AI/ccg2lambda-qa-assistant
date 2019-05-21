PRINT_VERBOSE = True
SEND_TO_CLIENT = False  # Union[bool, Client], cannot specify it because of circular imports


def set_client(client):  # Union[bool, Client], cannot specify it because of circular imports
    global SEND_TO_CLIENT
    SEND_TO_CLIENT = client


def set_verbose(verbose: bool):
    global PRINT_VERBOSE
    PRINT_VERBOSE = verbose

    if PRINT_VERBOSE:
        info("This session will print verbose messages.")
    else:
        info("This session will not print verbose messages.")


def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30, 38):
            s1 = ''
            for bg in range(40, 48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')


def info(*args) -> None:
    print(*args)
    # noinspection PySimplifyBooleanCheck
    if SEND_TO_CLIENT is not False:
        # noinspection PyUnresolvedReferences
        SEND_TO_CLIENT.send('info', *args)


def announce(*args) -> None:
    print('\x1b[32m', *args, '\x1b[0m')


def warning(*args) -> None:
    print('\x1b[33m', *args, '\x1b[0m')


def error(*args) -> None:
    print('\x1b[1;37;41m', *args, '\x1b[0m')


def verbose(*args) -> None:
    if PRINT_VERBOSE:
        print('\x1b[1;90m', *args, '\x1b[0m')


verbose("Loaded package 'qalogging'")
