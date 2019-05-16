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
            "Who is the president of the United States in 2017 ?",
            "Who is Barack Obama ?"
            "Is Barack Obama a president?",
            "What do I want to eat for dinner ?"
            "Who is this person?",
            "The son of my mother is me",
            "Can you eat fish from 2018?",
            "When was the last snack?",
            "Where is the USA ?"
        ]
        [verbose(ast) for ast in convert(sentences)]
