from xml.etree import ElementTree


def visualize(tree: ElementTree, filename : str) -> None:
    """
    Creates an XML file to be used
    :param tree: the root of the tree
    :param filename: the name of the output file
    """
    a = ElementTree.ElementTree()
    a._setroot(tree)
    a.write(filename)
