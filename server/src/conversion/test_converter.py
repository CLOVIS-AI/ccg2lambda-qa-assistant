from unittest import TestCase

from .converternaturaltosparql import *

from lxml import etree


class TestWrapper(TestCase):
    def setUp(self):
        self.converter = ConverterNaturalToSPARQL("What are the languages in China ? \n Who is John Watson ? \
                                                    \n How many dogs were in my house in 2014 ?")

    def test_makeRequest(self):
        self.converter.convert()
        self.converter.visualize_semantic()

        parser = etree.XMLParser(ns_clean=True)
        tree = etree.parse(PATH_TO_TMP + "/sentences.sem.xml", parser)

        print(etree.tostring(tree, pretty_print=True))
