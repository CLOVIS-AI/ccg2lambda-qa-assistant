#
# This is the main file of the software.
#


def main():
    print('Starting ccg2lambda QA Assistant Server...')

    # Starting the server
    from network import server

    # Here we can register commands if we ever need to

    # The server starts listening to requests
    server.run()
    # The above method is blocking: the code never reaches this point


main()
