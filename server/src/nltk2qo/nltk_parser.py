from nltk.sem.logic import ExistsExpression, Expression, AndExpression, ApplicationExpression, EqualityExpression

from nltk2qo.sentence import Sentence
from qalogging import error


def read_expressions(value: Expression, sentence: Sentence):
    """
    Recursively reads an Expression and modifies the given Sentence to reflect what is seen.
    :param value: The Expression that needs to be parsed.
    :param sentence: The Sentence output.
    """
    t = type(value)

    if t == ExistsExpression:
        sentence.add(value.variable.name)
        read_expressions(value.term, sentence)
    elif t == AndExpression:
        read_expressions(value.first, sentence)
        read_expressions(value.second, sentence)
    elif t == ApplicationExpression:
        sentence.add_tag(value.function.variable.name, value.argument.variable.name)
    elif t == EqualityExpression:
        sentence.add_link(value.second.variable.name,
                          value.first.argument.variable.name,
                          value.first.function.variable.name)
    else:
        error("Type [", t, "] unknown, aborting.")
        raise Exception("I do not know how to handle the type [", t, "] !")
