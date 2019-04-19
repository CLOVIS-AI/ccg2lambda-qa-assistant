package network

import EOL_CHAR
import SEPARATION_CHAR
import java.io.PrintWriter

data class Command(val name: String, val params: List<String>) {

    constructor(name: String, vararg params: String) : this(name, params.toList())

    fun writeTo(writer: PrintWriter) {
        writer.print(name)

        params.forEach { param ->
            writer.print(SEPARATION_CHAR)
            writer.print(param)
        }

        writer.print(EOL_CHAR)
        writer.flush()
    }

}