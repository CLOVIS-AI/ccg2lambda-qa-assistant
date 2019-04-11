# Python Networking

## Use from Python

The server is automatically instantiated by the module when it is imported.

    from network import server

To register a command:

    def ping(server, client, word)
        client.send("pong", word)
    
    server.register_command("ping", ping)

In this example, whenever the "ping" command is received, it will run the function `ping`.

The given arguments are `server` which represents the server instance, `client` which represents the particular client
that sent the request, then any parameters you expect.

You can therefore create any method with any arguments you expect:

    def something(server, client, first, second, third):
        pass

## Use as a client

This module is essentially a server that listens on port 12800 (can be changed in `__init__.py`).

The protocol to send messages is as follows:
 - Messages are separated by end-of-line characters (`\n`)
 - Messages are constituted of a command name, and of parameters, separated by paragraph characters (`§`, can be 
   changed in `__init__.py`).

Examples:

 - `ping§something` is a valid message: `ping` is the command name, and `something` is the parameter.
 - `hello§first§second` is a valid message: `hello` is the command name, and `first` and `second` are the parameters.

Because of these rules, neither the `\n` nor `§` characters are allowed in command names or parameters. This module does
NOT verify their absence: it is your responsibility to remove them.