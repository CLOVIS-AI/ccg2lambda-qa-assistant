from unittest import TestCase

from conversion.converter import convert
from nltk2qo.converter import nltk_to_query_objects


class TestNltk_to_query_objects(TestCase):

    def test_nltk_to_query_objects(self):
        test_questions = open("conversion/test_converter_questions.txt", "r")
        sentences = [s.replace("\n", "") for s in test_questions.readlines()]
        test_questions.close()

        nltk_to_query_objects(convert(sentences))
