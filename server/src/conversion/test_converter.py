from unittest import TestCase

from lxml import etree

from .converternaturaltosparql import *


class TestConvertCcg2lambda(TestCase):
    def setUp(self):
        init_paths()
        test_questions = open("conversion/test_converter_questions.txt", "r")
        self.sentences: str = test_questions.read()
        test_questions.close()

    def test_makeRequest(self):
        clean_tmp_dir()

        # Converting the sentences with ccg2lambda
        success = convert(self.sentences)
        self.assertTrue(success)
        visualize_semantic()

        # Checking the output files
        self.assertTrue(os.path.isdir(TMP))
        self.assertFalse(len(os.listdir(TMP)) == 0)
        events = ("start", "end")
        context = etree.iterparse(TMP + "/sentences.sem.xml", events=events, tag="semantics")
        for action, elem in context:
            self.assertEqual("success", elem.attrib["status"])

        # clean_tmp_dir()

    def test_cleanUp(self):
        # Cleaning temporary folders
        clean_tmp_dir()
        self.assertEqual(0, len(os.listdir(TMP)))
