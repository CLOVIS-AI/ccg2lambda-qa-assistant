# Expects Sentence structure to be working as intended.

from unittest import TestCase
from nltk2qo.converter import nltk_to_query_objects
from conversion.converter import convert
from sparql.queryBuilder.query_builder import QueryBuilder


class TestQueryBuilder(TestCase):

    def setUp(self) -> None:
        sentence_string = ["What are the presidents of the USA?"]
        sentence_object = nltk_to_query_objects(convert(sentence_string))
        self.__queryBuilder = QueryBuilder(sentence_object[0])

    def test_build(self):
        self.__queryBuilder.build()
