from unittest import TestCase

from conversion import init_paths
from .converter import *
from qalogging import verbose


class TestConvertCcg2lambda(TestCase):

    def setUp(self):
        init_paths()
        test_questions = open("conversion/test_converter_questions.txt", "r")
        self.sentences = test_questions.readlines()
        test_questions.close()

    def test_convert(self):
        [verbose(ast) for ast in convert(self.sentences, output_file = True)]
