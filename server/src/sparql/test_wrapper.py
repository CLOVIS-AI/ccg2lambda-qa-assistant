from unittest import TestCase

from sparql.wrapper import Wrapper


class TestWrapper(TestCase):
    def setUp(self):
        file = open("sparql/query.sparql")
        self.wrapper = Wrapper(
            "https://query.wikidata.org/sparql",
            file.read())
        file.close()

    def test_makeRequest(self):
        expected_result = open("sparql/test_wrapper_expected_result.txt", "r")
        actual_result = self.wrapper.make_request()
        self.assertEqual(expected_result.read(), actual_result)
        expected_result.close()
