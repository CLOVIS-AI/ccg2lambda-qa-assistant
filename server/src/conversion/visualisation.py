from xml.etree import ElementTree
import os


def visualize(tree: ElementTree, filename: str) -> None:
    """
    Create a visualization of the parsed semantic representation of the sentences in html format
    The output file is found in the folder ccg2lambda-qa-assistant/server/src/ by default
    :param tree: the root of the XML Etree tree
    :param filename: the name of the output file, need to be a .html
    """
    create_XML_file(tree, "sentences.sem.xml")
    os.system(
        "python ../../ccg2lambda/scripts/visualize.py sentences.sem.xml > " +
        filename)


def create_XML_file(tree: ElementTree, filename: str) -> None:
    """
    Creates an XML file to be used
    :param tree: the root of the tree
    :param filename: the name of the output file
    """
    a = ElementTree.ElementTree()
    a._setroot(tree)
    a.write(filename, encoding="utf-8")
