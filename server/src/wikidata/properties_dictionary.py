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
        Fills a dictionary of properties under the of a .txt.
        """
        dictionary = open("wikidata/dictionary.txt", "w")
        wrapper = Wrapper("https://query.wikidata.org/sparql", "wikidata/propertiesQuery.sparql")
        result = wrapper.make_request_dictionary()
        dictionary.write(result)
        dictionary.close()

    def load_dictionary(self):
        """
        Some of the names have homonyms: this program doesn't manage it (yet?)
        """
        f = open("wikidata/dictionary.txt", "r")
        for line in f.readlines():
            if not self.__dictionary.__contains__(line.split(':')[0]):
                self.__dictionary[line.split(':')[0]] = line.split(':')[1].split('\n')[0]
        f.close()

    def __getitem__(self, item):
        if self.__dictionary.__contains__(item):
            return self.__dictionary[item]
        else:
            return None
