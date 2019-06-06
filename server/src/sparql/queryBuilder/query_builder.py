from sparql.wrapper import Wrapper
from nltk2qo.sentence import Sentence
from qalogging import verbose, info, announce, error
from wikidata.wikicode_getter import get_all_q_codes, get_all_p_codes
from nltk2qo.event import Event
from nltk2qo.entity import Entity


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
        self.__triples = []
        self.__qm_found = False
        file.close()

    def __request(self) -> str:
        """
        Executes the query using the SPARQL wrapper.
        :return: the result of the query (JSON formatted string)
        """
        # closes the request with the end curly brace
        wrapper = Wrapper(
            "https://query.wikidata.org/sparql",
            self.__query + " }")
        return wrapper.make_request()

    @staticmethod
    def __get_tags(tag_lists: Entity) -> str:
        """
        Creates a single string from a list of tags of an event
        :param tag_lists: event
        :return: string
        """
        result = ""
        name_tag = (tag for tag in tag_lists.tags if tag.startswith('_'))
        if name_tag:
            for tag in name_tag:
                result += tag
            result.replace('_', ' ')

            return result[1:]
        else:
            return None

    def __manage_qm(self, event: Event) -> None:
        """
        Manages the question marker depending on the verb
        :param event: the event
        """
        # Create an empty triple
        subj = pred = obj = "#"
        from wikidata.ask import ask_client
        if "_be" in event.tags:
            for var in event.variables:
                # we define the property linked to the searched object
                # as the accusative of the qm event
                if var[0] == "Acc":
                    # TODO: add Conj management here
                    attr = self.__get_tags(var[1])
                    pred = self.__namedVar[var[1].id] = "wdt:" + ask_client(
                        get_all_p_codes(attr))
                # TODO: Manage more precises cases
                else:
                    obj = self.__namedVar[var[1].id] = "?item"
        else:
            # TODO: make the verb under its common noun form
            attr = self.__get_tags(event)
            pred = self.__namedVar[event.id] = "wdt:" + ask_client(
                get_all_p_codes(attr))
            for var in event.variables:
                if var[0] == "Acc":
                    attr = self.__get_tags(var[1])
                    subj = self.__namedVar[var[1].id] = "wd:" + ask_client(
                        get_all_q_codes(attr))
                # TODO: Manage more precises cases
                else:
                    obj = self.__namedVar[var[1].id] = "?item"

        self.__triples.append((subj, pred, obj))

    def __create_new_event_triple(self, event: Event, attr: str) -> None:
        """
        Creates a new triple from a event with a tag (an event has a tag if it is a verb)
        :param event:
        :param attr:
        """
        subj = pred = obj = "#"
        from wikidata.ask import ask_client

        pred = self.__namedVar[event.id] = "wdt:" + ask_client(
            get_all_p_codes(attr))
        for var in event.variables:
            subj_or_obj = "#"
            # if the var has already been found, just fetch its value
            # TODO: add Conj management
            if var[1].id in self.__namedVar:
                subj_or_obj = self.__namedVar[var[1]]
            else:
                attr = self.__get_tags(var[1])
                subj_or_obj = self.__namedVar[var[1].id] = "wd:" + ask_client(
                    get_all_q_codes(attr))

            if var[0] == "Acc":
                subj = subj_or_obj
            # TODO: Manage more precises cases
            else:
                obj = subj_or_obj

        self.__triples.append((subj, pred, obj))

    def __search_or_create_triple(self, pred: str, subj: str):
        """
        Searches and completes an existing predicate or creates a new to-be-completed one
        :param pred: the predicate
        :param subj: the subject (allegedly cannot be an object, but has to be proven
        """
        found_triple = False
        for index, triple in enumerate(self.__triples):
            if pred == triple[1] and triple[0] == "#":
                found_triple = True
                self.__triples[index] = (subj, triple[1], triple[2])

        # this program does not manage objects fetching for now
        if not found_triple:
            self.__triples.append((subj, pred, '#'))

    def __manage_special_tag_event(self, event: Event) -> None:
        """
        Fetches the predicate and the subject of an event with a special tag (e.g.: _of, _in)
        :param event: the event
        """
        from wikidata.ask import ask_client
        pred = subj = pred_or_subj = '#'
        for var in event.variables:
            is_subj = var[0] == "Subj"

            if var[1].id in self.__namedVar:
                pred_or_subj = self.__namedVar[var[1].id]
            else:
                attr = self.__get_tags(var[1])
                pred_or_subj = self.__namedVar[var[1].id] = ("wdt:" + ask_client(
                    get_all_p_codes(attr))) if is_subj else ("wd:" + ask_client(get_all_q_codes(attr)))

            # Subjects of these events are predicates.
            if is_subj:
                pred = pred_or_subj
            # TODO: Manage more precise cases
            else:
                subj = pred_or_subj

        self.__search_or_create_triple(pred, subj)

    def __complete_triple(self, event: Event) -> None:
        """
        Completes a triple are create a to-be-completed one in order
        :param event:
        :return:
        """
        contains_special_tag = False
        # Search for special tags like _of or _in
        for var in event.variables:
            if var[0].startswith('_'):
                contains_special_tag = True
        # manages the var
        if contains_special_tag:
            self.__manage_special_tag_event(event)

    def __manage_event(self, event: Event) -> None:
        """
        Manages any kind of event that does not contains the question marker
        :param event: the event
        """
        attr = self.__get_tags(event)
        # if the event is not none, hence it is a verb, hence we need a new
        # triple
        if attr != "":
            self.__create_new_event_triple(event, attr)
        else:
            self.__complete_triple(event)

    def __fill_dictionary(self) -> None:
        """
        gives a var name for each determined object of the sentence.
        """
        for event in self.__sentence.events:
            if not self.__qm_found:
                for var in event.variables:
                    if var[1] == self.__sentence.main:
                        verbose("Found question marker.")
                        self.__qm_found = True
                if self.__qm_found:
                    self.__manage_qm(event)
                    self.__sentence.events.remove(event)
                    # as the qm event has to be the first event to be worked with, we need to iterate on the
                    # remaining events
                    self.__fill_dictionary()
                    break
            else:
                self.__manage_event(event)

    def build(self):
        """
        Add triples to the basic query template (sparql/queryBuilder/query_template.sparql) and sends the request
        :return: the result of the request.
        """
        verbose("Filling variables dictionary...")
        self.__fill_dictionary()
        for triple in self.__triples:
            self.__query += ' ' + triple[0] + ' ' + triple[1] + \
                            ' ' + triple[2] + ' .'
        announce("Sending query: " + self.__query)
        info("The answer is: " + self.__request())
