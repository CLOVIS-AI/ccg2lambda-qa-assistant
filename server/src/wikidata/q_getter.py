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


def get_q_number(item: str):
    """
    gets a list of objects found on Wikidata based on a searched string.
    :param item: string of the search
    :return: json containing the result
    """
    resp = get('https://www.wikidata.org/w/api.php', {
        'action': 'wbsearchentities',
        'language': 'en',
        'type': 'item',
        'search': item,
        'format': 'json'

    }).json()

    return resp


def get_p_number(search: str):
    """

    :param search:
    :return:
    """
    resp = get('https://www.wikidata.org/w/api.php',{
        'action': 'wbsearchentities',
        'language': 'en',
        'type': 'property',
        'search': search,
        'format': 'json'
    }).json()

    return resp


def wikipedia_suggestion(words: str):
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
        except wikipedia.exceptions.PageError:
            return "[ERROR]: \"" + words + "\" does not match any pages. Try another name!"

    print("page = " + page.title)
    return page.title


def get_all_q_codes(words: str):
    """
    gets the list of codes relevant to the searched words passed in parameters.
    :param words: string of searched words
    :return: list of q-codes with, for each, a short description of the linked page.
    """
    title = wikipedia_suggestion(words)
    if not title.startswith("[ERROR]"):
        answer = get_q_number(item=title)
        for string in answer['search']:
            try:
                desc = string['description']
            except KeyError:
                desc = "No description available"
            print(string['id'] + " : " + desc)
    else:
        print(title)


@DeprecationWarning
def get_q_number_from_word(item: str):
    """
    Currently unused function. Kept in order to have the key workds of the action wbgetentities
    :param item:
    :return:
    """
    resp = get('https://www.wikidata.org/w/api.php', {
        'action': 'wbgetentities',
        'languages': 'en',
        'sites': 'enwiki',
        'titles': item,
        'props': 'info',
        'normalize': '1',
        'format': 'json'
    }).json()

    return resp

# get_all_q_codes(words="Aristude Briand")
get_all_q_codes("Bertrand")
# print(get_p_number("location"))


# print(get_q_number2("Q30"))
# print(get_q_number_from_word("homme"))
