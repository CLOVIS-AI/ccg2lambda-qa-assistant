from SPARQLWrapper import SPARQLWrapper, JSON


#
# query wrapper to request to the source
#


class Wrapper:

    def __init__(self, url, query):
        self._wrapper = SPARQLWrapper(url)
        self.__query_path = query

    def make_request(self):
        file = open(self.__query_path, "r")
        self._wrapper.setQuery(file.read())

        self._wrapper.setReturnFormat(JSON)
        results = self._wrapper.query().convert()

        for result in results["results"]["bindings"]:
            print(result)

        file.close()
