from unittest import TestCase

from .converternaturaltosparql import ConverterNaturalToSPARQL

class TestWrapper(TestCase):
    def setUp(self):
        self.converter = ConverterNaturalToSPARQL("What are the languages in China ?")

    def test_makeRequest(self):
        self.converter.Convert()
