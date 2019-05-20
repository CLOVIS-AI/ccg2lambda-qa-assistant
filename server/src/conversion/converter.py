from typing import List, Tuple, Any

from depccg.printer import to_jigg_xml
from depccg.semantics.ccg2lambda import parse
from depccg.semantics.ccg2lambda.logic_parser import lexpr
from depccg.token import annotate_using_spacy, Token
from depccg.tree import Tree
from nltk import Expression

from conversion import depccg_parser
from conversion.paths import TEMPLATE
from qalogging import info, verbose, announce
from conversion import visualisation


def __annotate_spacy(sentences: List[str]) -> Tuple[List[List[Token]], List[List[str]]]:
    """
    Annotates a list of sentences in English, using spaCy.
    :param sentences: A list of English sentences.
    :return: a tuple of a list of all annotated tokens in each sentence, and a list of each word in each sentence.
    """
    info(" › spaCy: annotating...")
    return annotate_using_spacy([sentence.split(" ") for sentence in sentences], tokenize=True)


def __convert_to_ccg(sentences: List[List[str]]) -> List[List[Tuple[Tree]]]:
    """
    Converts a list of sentences (where each sentence is a list of words) to a list of CCG trees, where each tree
    corresponds to the sentence with the same index in the given parameter, using DepCCG.
    :param sentences: A list of (sentence: list of words)
    :return: A list of CCG trees
    """
    info(" › DepCCG: English 🠦 CCG")
    return depccg_parser.parse_doc(sentences)


def __ccg_to_lambda(ccg: List[List[Tuple[Tree]]], annotated_sentences: List[List[Token]]) -> Any:
    """
    Converts a list of CCG trees to a list of λ-expressions, using ccg2lambda.
    :param ccg: A list of CCG trees
    :param annotated_sentences: A list of all annotated tokens in each of the given sentences
    :return: A list of λ-expressions.
    """
    info(" › ccg2lambda: CCG 🠦 λ")
    return to_jigg_xml(ccg, annotated_sentences)


def __lambda_to_drs(lambda_expressions: Any) -> List[List[str]]:
    """
    Converts a list of λ-expressions to a list of multiple DRS representations.
    :param lambda_expressions: A list of λ-expressions.
    :return: A list in which each element is the list of parsed DRS representations for each sentence.
    """
    info(" › ccg2lambda: λ 🠦 DRS")
    return parse.parse(lambda_expressions, TEMPLATE)[1]


def __drs_to_python(all_drs: List[List[str]]) -> List[Expression]:
    """
    Parses a list of DRS representations into a list of corresponding Python objects.
    :param all_drs: A list of DRS representations.
    :return: A list of Expressions, which are Python objects that represent the sentence.
    """
    info(" › nltk: DRS 🠦 Python objects")
    return [lexpr(drs) for sentence in all_drs for drs in sentence]


def convert(sentences: List[str]) -> List[Expression]:
    """
    Converts a list of questions to an Abstract Syntax Tree (AST), using:
     - spaCy to annotate each word with its grammatical class,
     - depccg to convert the natural language to a CCG tree,
     - ccg2lambda to convert the CCG tree to a DRS representation,
     - nltk to parse that DRS into an AST represented in Python objects.

    :param sentences: a list of questions in English
    :exception if less than 1 sentence is provided
    :return a list of ASTs that each correspond to one of the given sentences (in the same order).
    """
    if len(sentences) < 1:
        raise Exception("Cannot run the pipeline with less than 1 sentence: " + str(len(sentences)))

    announce("Beginning conversion of", len(sentences), "sentences, the first one is [", sentences[0], "]")
    annotated_sentences, split_sentences = __annotate_spacy(sentences)
    ccg_of_each_sentence = __convert_to_ccg(split_sentences)
    print(annotated_sentences)
    lambda_expressions = __ccg_to_lambda(ccg_of_each_sentence, annotated_sentences)

    # visualisation.visualize(lambda_expressions, "sentences.xml")

    formulas = __lambda_to_drs(lambda_expressions)
    visualisation.visualize(lambda_expressions, "sentences.sem.xml")
    expr = __drs_to_python(formulas)
    verbose("Conversion done.")
    return expr
