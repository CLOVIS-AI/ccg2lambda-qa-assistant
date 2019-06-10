from typing import List

from nltk import Expression

from nltk2qo.nltk_parser import read_expressions
from nltk2qo.sentence import Sentence
from qalogging import verbose, info, warning


def __parse(nltk_output: Expression) -> Sentence:
    """
    Parses an Expression into a Sentence.
    :param nltk_output: A query object representing a Sentence, fully built.
    """
    verbose("Now parsing [", nltk_output, "]")
    sentence = Sentence()
    read_expressions(nltk_output, sentence)
    sentence.fix()

    verbose("Done with this sentence.")
    sentence.pretty_print()

    if sentence.main is None:
        warning("No Question Marker found! This sentence is not a question.")

    return sentence


def nltk_to_query_objects(nltk_output: List[Expression]) -> List[Sentence]:
    """
    Converts objects created by NLTK after the ccg2lambda pipeline into Query Objects.
    :param nltk_output: The output from the ccg2lambda pipeline.
    :return: A list of Sentences, as Query Objects.
    """
    info(" › nltk2qo: nltk Python Objects 🠦 Query Objects")
    sentences = [__parse(sentence) for sentence in nltk_output]

    verbose("Conversion to Query Objects done.")
    # display some stats about the conversion
    return sentences
