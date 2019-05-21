from sparql.wrapper import Wrapper

#
#   Dictionary reader and writer of Wikidata properties
#


class Dictionary:
    def __init__(self):
        self.__dictionary = {}

    @staticmethod
    def fill_dictionary_query():
        """
        Fills a dictionary of properties under the form of a .txt.
        """
        dictionary = open("wikidata/dictionary.txt", "w")
        wrapper = Wrapper("https://query.wikidata.org/sparql", "wikidata/propertiesQuery.sparql")
        result = wrapper.make_request_dictionary()
        dictionary.write(result)
        dictionary.close()

    def load_dictionary(self):
        """
        Fills a mapped object 'dictionary', which key is the name of the Wikidata property and which value is its
        P-code. Does not manage homonyms (e.g.: "location" has 2 different P-codes).
        """
        f = open("wikidata/dictionary.txt", "r")
        for line in f.readlines():
            if not self.__dictionary.__contains__(line.split(':')[0]):
                self.__dictionary[line.split(':')[0]] = line.split(':')[1].split('\n')[0]
        f.close()

    def __getitem__(self, item: str):
        """
        getter of the P-code via its property name. Dictionary has to be loaded before use.
        :param item: the name of the Wikidata property
        :return: the P-code of the property (string)
        """
        if self.__dictionary.__contains__(item):
            return self.__dictionary[item]
        else:
            return None
