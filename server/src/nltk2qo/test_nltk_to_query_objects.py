from unittest import TestCase

from conversion.converter import convert
from nltk2qo.converter import nltk_to_query_objects


class TestNltk_to_query_objects(TestCase):

    def test_nltk_to_query_objects(self):
        nltk_to_query_objects(convert(["This is a test."]))
