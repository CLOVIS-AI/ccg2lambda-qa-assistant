PRINT_VERBOSE = True


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


def announce(*args) -> None:
    print('\x1b[0;32;40m', *args, '\x1b[0m')


def warning(*args) -> None:
    print('\x1b[0;33;40m', *args, '\x1b[0m')


def error(*args) -> None:
    print('\x1b[1;37;41m', *args, '\x1b[0m')


def verbose(*args) -> None:
    if PRINT_VERBOSE:
        print('\x1b[1;30;40m', *args, '\x1b[0m')


verbose("Loaded package 'qalogging'")

if PRINT_VERBOSE:
    info("This session will print verbose messages.")
else:
    info("This session will not print verbose messages.")
