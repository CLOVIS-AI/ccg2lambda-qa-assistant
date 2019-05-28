from SPARQLWrapper import SPARQLWrapper, JSON


#
# query wrapper requesting to a specified endpoint.
#


class Wrapper:

    def __init__(self, url, query):
        self.__wrapper = SPARQLWrapper(url)
        self.__query = query

    def make_request(self):
        """
        Creates the request of the query given in its parameter and sends it to the URL.
        :return: result of the query
        """
        self.__wrapper.setQuery(self.__query)

        self.__wrapper.setReturnFormat(JSON)
        results = self.__wrapper.query().convert()

        string_result = ""
        # Will end by a new empty line.
        for result in results["results"]["bindings"]:
            string_result += result["itemLabel"]["value"] + "\n"

        return string_result
