from unittest import TestCase
from sparql.wrapper import Wrapper


class TestWrapper(TestCase):
    def setUp(self):
        self.wrapper = Wrapper("https://query.wikidata.org/sparql", "query.sparql")

    def test_makeRequest(self):
        self.wrapper.make_request()
