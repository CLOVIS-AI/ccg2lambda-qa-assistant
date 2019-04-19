package network

import java.io.Closeable
import java.io.PrintWriter
import java.net.Socket

// Adapted from https://www.baeldung.com/a-guide-to-java-sockets

class Server(ip: String, port: Int) : Closeable {

    private val socket = Socket(ip, port)
    private val output = PrintWriter(socket.getOutputStream(), false)
    private val input = socket.getInputStream().bufferedReader(Charsets.UTF_8)

    fun send(command: String, vararg params: String) = send(Command(command, *params))

    fun send(command: Command): Command {
        command.writeTo(output)
        return Command.readFrom(input)
                ?: Command("end", "The socket was closed")
    }

    override fun close() {
        input.close()
        output.close()
        socket.close()
    }
}