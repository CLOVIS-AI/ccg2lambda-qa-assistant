from nltk.sem.logic import ExistsExpression, Expression, AndExpression, ApplicationExpression, EqualityExpression, \
    AllExpression, IndividualVariableExpression

from nltk2qo.sentence import Sentence
from qalogging import error, warning, verbose


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
        sentence.add_tag(
            value.function.variable.name,
            value.argument.variable.name)
    elif t == EqualityExpression:
        first = type(value.first)
        if first == IndividualVariableExpression:  # (x1 = x2)
            sentence.mark_as_equal(
                value.first.variable.name,
                value.second.variable.name)
        elif first == ApplicationExpression:  # (link(e) = x)
            sentence.add_link(value.second.variable.name,
                              value.first.argument.variable.name,
                              value.first.function.variable.name)
        else:
            error(
                "Found an EqualityExpression but the first argument is a [",
                first,
                "], which is unforeseen!")
            raise Exception(
                "I do not know how to handle the type [", first, "] in a [", t, "] !")
    elif t == AllExpression:
        verbose("nltk2qo: Found a AllExpression")
        warning(
            "It looks like this sentence is a yes/no question, and they are not supported currently.")
    else:
        error("Type [", t, "] unknown, aborting.")
        raise Exception("I do not know how to handle the type [", t, "] !")
