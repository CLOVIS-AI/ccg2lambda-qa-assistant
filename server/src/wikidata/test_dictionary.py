from unittest import TestCase

from wikidata.properties_dictionary import Dictionary


class TestDictionary(TestCase):
    def test_fill_dictionary_query(self):
        """
        Must not be run from this file. Run instead from the global test section for dynamic paths reasons.
        """
        dictionary = Dictionary()
        dictionary.fill_dictionary_query()

    def test_load_dictionary(self):
        """
        Must not be run from this file. Run instead from the global test section for dynamic paths reasons.
        Considers that a dictionary exists
        """
        dictionary = Dictionary()
        assert dictionary.__getitem__("instance of") is None
        dictionary.load_dictionary()
        assert dictionary.__getitem__("instance of") == "P31"
        assert dictionary.__getitem__("discography") == "P358"

        # with synonyms
        assert dictionary.__getitem__("neighborhood") == "P276"
        assert dictionary.__getitem__("location") == "P276"
        assert dictionary.__getitem__("place held") == "P276"
