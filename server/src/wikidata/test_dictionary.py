from unittest import TestCase

from wikidata.properties_dictionary import Dictionary


class TestDictionary(TestCase):
    def test_fill_dictionary(self):
        dictionary = Dictionary("../res/HTML")
        dictionary.fill_dictionary()

    def test_load_dictionary(self):
        dictionary = Dictionary("../res/HTML")
        assert dictionary.get_dictionary() == {}
        dictionary.load_dictionary()
        assert dictionary.get_dictionary() != {}
