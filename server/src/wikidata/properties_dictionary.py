import os
import bs4

#
#   Dictionary reader and writer of Wikidata properties
#


class Dictionary:
    def __init__(self, html_path):
        self.__html_path = html_path
        self.__dictionary = {}

    # temporary solution, may change in the future
    # fills a dictionary under the form of a txt. Uses html pages https://tools.wmflabs.org/prop-explorer/

    def fill_dictionary(self):
        dictionary = open("dictionary.txt", "w")
        for filename in os.listdir(self.__html_path):
            if filename.endswith(".html"):
                f = open(self.__html_path + '/' + filename)
                soup = bs4.BeautifulSoup(f.read(), 'lxml')
                print("Found file: " + filename)
                for tab_line in soup.find_all("div", "rt-tr-group"):
                    code = tab_line.contents[0].contents[1].contents[0].contents[0].string
                    # retrieving data from a tab that can have empty cells
                    # Proper codes are at least of length 3
                    if len(code) > 2:
                        label = tab_line.contents[0].contents[2].contents[0].contents[0].string
                        dictionary.write(label + ":" + code + "\n")
                f.close()
        dictionary.close()

    def load_dictionary(self):
        f = open("dictionary.txt", "r")
        for line in f.readlines():
            self.__dictionary[line.split(':')[0]] = line.split(':')[1].split('\n')[0]
        f.close()

    def get_dictionary(self):
        return self.__dictionary
