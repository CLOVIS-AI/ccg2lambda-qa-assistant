from sparql.wrapper import Wrapper
from nltk2qo.sentence import Sentence
from qalogging import error, verbose
from wikidata.wikicode_getter import get_all_q_codes, get_all_p_codes
from wikidata.ask import ask_client
from nltk2qo.event import Event


class QueryBuilder:

    def __init__(self, sentence: Sentence):
        """
        Query Builder class containing a query, a Sentence object (result from the parsing of ccg2lambda and
        nltk_parser)
        and a dictionary linking for each word its var string in SPARQL.
        :param sentence:
        """
        file = open("sparql/queryBuilder/query_template.sparql", "r")
        self.__query = file.read()
        self.__sentence = sentence
        self.__namedVar = {}
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

    def __manage_qm(self, event: Event) -> None:
        """
        Manages the question marker depending on the verb
        :param event: the event
        :return: true if the questionMarker is found, false otherwise
        """
        if "_be" in event.tags:
            for var in event.variables:
                # we define the property linked to the searched object
                # as the accusative of the qm event
                if var[0] == "Acc":
                    # add Conj management
                    attr = var[1].tags[0].split('_')[1]
                    self.__namedVar[attr] = "wdt:" + ask_client(
                        get_all_p_codes(attr))
                else:
                    self.__namedVar[var[1].tags[0]] = "?item"
        else:
            for var in event.variables:
                


    def __fill_dictionary(self) -> None:
        """
        gives a var name for each determined object of the sentence.
        """
        verbose("Filling variables dictionary...")
        question_marker = self.__sentence.main
        for event in self.__sentence.events:
            qm = False
            for var in event.variables:
                if var[1] == question_marker:
                    verbose("Found question marker.")
                    qm = True
            if qm:
                self.__manage_qm(event)
            # elif event.tags[0] == "":


        error(str(self.__namedVar))

    def build(self):
        """
        Add triples to the basic query template (sparql/queryBuilder/query_template.sparql) and sends the request
        :return: the result of the request.
        """
        self.__fill_dictionary()
        self.__sentence.pretty_print()
        # for e in self.__sentence.events:
        #   for v in e.variables:
        #      for tag in v[1].tags:
        #         error(tag)
