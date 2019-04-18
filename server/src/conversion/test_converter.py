from unittest import TestCase

from .converternaturaltosparql import *

from lxml import etree

import os


class TestConvertCcg2lambda(TestCase):
    def setUp(self):
        test_questions = open("conversion/test_converter_questions.txt", "r")
        self.sentences = test_questions.read()

    def test_makeRequest(self):
        cleanTmpDir()

        # Converting the sentences with ccg2lambda
        succes = convert(self.sentences)
        self.assertTrue(succes)
        visualize_semantic()

        # Checking the output files
        self.assertTrue(os.path.isdir(PATH_TO_TMP))
        self.assertFalse(len(os.listdir(PATH_TO_TMP)) == 0)
        events = ("start", "end")
        context = etree.iterparse(PATH_TO_TMP + "/sentences.sem.xml", events = events, tag = "semantics")
        for action, elem in context:
            self.assertEqual("success", elem.attrib["status"])

        cleanTmpDir()

    def test_cleanUp(self):
        # Cleaning temporary folders
        cleanTmpDir()
        self.assertEqual(0, len(os.listdir(PATH_TO_TMP)))
