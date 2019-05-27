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
    corresponds to the sentence with the same index in the given parameter, using depccg.
    :param sentences: A list of (sentence: list of words)
    :return: A list of CCG trees
    """
    info(" › depccg: English 🠦 CCG")
    return depccg_parser.parse_doc(sentences)


def __ccg_to_jigg_xml(CCG: List[List[Tuple[Tree]]], annotated_sentences: List[List[Token]]) -> Any:
    """
    Converts a list of CCG trees to jigg xml format.
    :param CCG: A list of CCG trees
    :param annotated_sentences: A list of all annotated tokens in each of the given sentences
    :return: A list of CCG trees in jigg xml.
    """
    info(" › ccg2lambda: CCG 🠦 CCG in Jigg XML")
    return to_jigg_xml(CCG, annotated_sentences)


def __ccg_jigg_xml_to_lambda(ccg_trees_jigg_xml: Any) -> List[List[str]]:
    """
    Converts a list of CCG trees to a list of λ-expressions, using ccg2lambda and the TEMPLATE file specified in
    the paths.py file.
    :param ccg_trees_jigg_xml: A list of CCG trees in jigg xml format.
    :return: A list in which each element is the list of parsed semantic representations for each sentence.
    """
    info(" › ccg2lambda: CCG in Jigg XML 🠦 λ")
    return parse.parse(ccg_trees_jigg_xml, TEMPLATE)[1]


def __lambda_to_python(all_lambda: List[List[str]]) -> List[Expression]:
    """
    Parses a list of lambda representations into a list of corresponding Python objects.
    :param all_lambda: A list of λ-expressions.
    :return: A list of Expressions, which are Python objects that represent the sentence.
    """
    info(" › nltk: λ 🠦 Python objects")
    return [lexpr(drs) for sentence in all_lambda for drs in sentence]


def convert(sentences: List[str], output_file=False) -> List[Expression]:
    """
    Converts a list of questions to an Abstract Syntax Tree (AST), using:
     - spaCy to annotate each word with its grammatical class,
     - depccg to convert the natural language to a CCG tree,
     - ccg2lambda to convert the CCG tree to a λ expressions,
     - nltk to parse that λ-expressions into an AST represented in Python objects.

    :param output_file: if True, will output an xml file of the parsed sentences
    :param sentences: a list of questions in English
    :exception if less than 1 sentence is provided
    :return a list of ASTs that each correspond to one of the given sentences (in the same order).
    """
    if len(sentences) < 1:
        raise Exception("Cannot run the pipeline with less than 1 sentence: " + str(len(sentences)))

    announce("Beginning conversion of", len(sentences), "sentences, the first one is [", sentences[0], "]")
    annotated_sentences, split_sentences = __annotate_spacy(sentences)
    ccg_of_each_sentence = __convert_to_ccg(split_sentences)
    lambda_expressions = __ccg_to_jigg_xml(ccg_of_each_sentence, annotated_sentences)

    formulas = __ccg_jigg_xml_to_lambda(lambda_expressions)

    # Creates an XML file to be used
    if output_file:
        # Can be used in ccg2lambda python script visualize.py to output sentences.html to give better overview
        info("Creating visualisation in file sentences.sem.xml")
        visualisation.visualize(lambda_expressions, "sentences.sem.xml")

    expr = __lambda_to_python(formulas)
    verbose("Conversion done.")
    return expr
