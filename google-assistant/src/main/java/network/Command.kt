package network

import EOL_CHAR
import SEPARATION_CHAR
import utils.get
import java.io.BufferedReader
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

    companion object {

        fun readFrom(reader: BufferedReader): Command? = splitLine(reader)?.let { words ->
            Command(words[0], words[1 until words.size])
        }

        private fun splitLine(reader: BufferedReader) = reader.readLine()?.split(SEPARATION_CHAR)

    }
}