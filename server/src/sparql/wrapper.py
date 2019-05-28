from SPARQLWrapper import SPARQLWrapper, JSON


#
# query wrapper requesting to a specified endpoint.
#


class Wrapper:

    def __init__(self, url, query_path):
        self._wrapper = SPARQLWrapper(url)
        self._query_path = query_path

    def make_request(self):
        """
        Creates the request of the query given in its parameter and sends it to the URL.
        :return: result of the query
        """
        file = open(self._query_path, "r")
        self._wrapper.setQuery(file.read())

        self._wrapper.setReturnFormat(JSON)
        results = self._wrapper.query().convert()

        string_result = ""
        # Will end by a new empty line.
        for result in results["results"]["bindings"]:
            string_result += result["itemLabel"]["value"] + "\n"

        file.close()
        return string_result
