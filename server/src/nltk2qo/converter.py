from typing import List

from nltk import Expression

from nltk2qo.nltk_parser import read_expressions
from nltk2qo.sentence import Sentence
from qalogging import verbose, info


def __parse(nltk_output: Expression) -> Sentence:
    """
    Parses an Expression into a Sentence.
    :param nltk_output: A query object representing a Sentence, fully built.
    """
    verbose("Now parsing [", nltk_output, "]")
    sentence = Sentence()
    read_expressions(nltk_output, sentence)
    verbose("Done with this sentence.")
    sentence.pretty_print()
    return sentence


def nltk_to_query_objects(nltk_output: List[Expression]) -> List[Sentence]:
    """
    Converts objects created by NLTK after the ccg2lambda pipeline into Query Objects.
    :param nltk_output: The output from the ccg2lambda pipeline.
    :return: A list of Sentences, as Query Objects.
    """
    info("Beginning conversion to Query Objects...")
    sentences = [__parse(sentence) for sentence in nltk_output]

    info("Conversion to Query Objects done.")
    # display some stats about the conversion
    return sentences
