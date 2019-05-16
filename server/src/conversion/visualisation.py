from xml.etree import ElementTree


def visualize(tree: ElementTree, filename):
    a = ElementTree.ElementTree()
    a._setroot(tree)
    a.write(filename)
