from unittest import TestCase

from conversion import init_paths
from .converter import *


class TestConvertCcg2lambda(TestCase):

    def setUp(self):
        init_paths()
        test_questions = open("conversion/test_converter_questions.txt", "r")
        self.sentences = test_questions.read()
        test_questions.close()

    def test_convert(self):
        sentences = [
            "This is a test.",
            "Is Barack Obama a president?",
            "Who is this person?",
            "The son of my mother is me",
            "Can you eat fish?"
        ]
        [verbose(ast) for ast in convert(sentences)]
