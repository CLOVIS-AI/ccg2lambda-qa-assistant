# ****Information to be known****
# This packages contains a very user-oriented way to fetch possible q-codes. It is pretty slow, however it is
# the most precise pipeline we found. Even though our requests could be way faster, we might lose nearmatching and
# context with our results.
# If you are interested in a way to run this program faster, please look towards the actions "wbsearchentities",
# "wbgetentities" and "query" (with search filter) of the Wikidata API as they are arguably the most efficient actions
# possible as long as you use only them.


from requests import get
# wikipedia pages fetcher
import wikipedia
# suppresses warning of other libs (that we didn't raise ourselves)
import warnings
from qalogging import verbose, error
from typing import List


def __get_wikidata_code(searched_words: str, object_type: str) -> str:
    """
    Gets a list of objects found on Wikidata based on a searched string.
    :param searched_words: string of the search
    :param object_type: string reprensentif the type of the search. Must be either 'item' or 'property'
    :return: json (inside a string) containing the result of the query
    """
    resp = get('https://www.wikidata.org/w/api.php', {
        'action': 'wbsearchentities',
        'language': 'en',
        'type': object_type,
        'search': searched_words,
        'format': 'json',
        'limit': '10'
    }).json()

    return resp


def __wikipedia_suggestion(words: str) -> str:
    """
    returns title of wikipedia page resulting of a search on words var
    :param words: the searched words
    :return: wikipedia page URL, None if not found
    """
    # ignores warning from Wikipedia package about its use of bs4
    warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')

    try:
        page = wikipedia.page(words)
    except wikipedia.exceptions.DisambiguationError as e:
        page = wikipedia.page(e.options[0])
    except wikipedia.exceptions.PageError:
        try:
            suggestion = wikipedia.suggest(words)
            page = wikipedia.page(suggestion)
        except (wikipedia.exceptions.PageError, IndexError, ValueError):
            return "[ERROR]: Item \"" + words + \
                "\" does not match any pages. Try another id!"

    verbose("Wikipedia page found: " + page.title)
    return page.title


def get_all_q_codes(words: str) -> List:
    """
    gets the list of items codes relevant to the searched words passed in parameters.
    :param words: string of searched words
    :return: list of q-codes with, for each, a short description of the linked page.
    """
    # searches only on wikipedia network for now, as it is *usually* more efficient than Wikidata.
    # Might propose later to the user to choose between Wikipedia *and*
    # Wikidata results.
    title = __wikipedia_suggestion(words)
    items = []
    if not title.startswith("[ERROR]"):
        answer = __get_wikidata_code(searched_words=title, object_type="item")
        for string in answer['search']:
            try:
                desc = string['description']
            except KeyError:
                desc = "No description available"
            items.append((string['id'], string['title'], desc, string['url']))
        return items
    else:
        error(title)
        return items


def get_all_p_codes(words: str) -> List:
    """
    gets the list of properties codes relevant to the searched words passed in parameters.
    :param words: string of searched words
    :return: list of p-codes with, for each, a short description of the linked page.
    """
    answer = __get_wikidata_code(searched_words=words, object_type="property")
    properties = []
    for string in answer['search']:
        try:
            desc = string['description']
        except KeyError:
            desc = "No description available"
        properties.append((string['id'], string['label'], desc, string['url']))

    if not properties:
        error("[ERROR]: Property \"" + words +
              "\" does not match any pages. Try another id!")
    return properties
