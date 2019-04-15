from unittest import TestCase
from sparql.wrapper import Wrapper


class TestWrapper(TestCase):
    def setUp(self):
        self.wrapper = Wrapper("https://query.wikidata.org/sparql", "query.sparql")

    def test_makeRequest(self):
        expected_result = open("test_wrapper_expected_result.txt", "r")
        actual_result = self.wrapper.make_request()
        self.assertEqual(expected_result.read(), actual_result)
        #print(actual_result)
        expected_result.close()
