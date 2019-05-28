from sparql.wrapper import Wrapper
from nltk2qo.sentence import Sentence


class QueryBuilder:

    def __init__(self, sentence: Sentence):
        file = open("query_template.sparql", "r")
        self.__query = file.read()
        self.__sentence = sentence
        file.close()

    def __request(self) -> str:
        """
        Executes the query using the SPARQL wrapper.
        :return: the result of the query (JSON formatted string)
        """
        # closes the request with the end curly brace
        wrapper = Wrapper(
            "https://query.wikidata.org/sparql",
            self.__query + "}")
        return wrapper.make_request()
