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
        i = 0
        for ast in convert([s.replace("\n", "") for s in self.sentences], output_file=True):
            verbose(str(i) + " - " + str(ast))
            i += 1
