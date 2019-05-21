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


def get_p_number(property: str):
    """

    :param property:
    :return:
    """
    resp = get('https://www.wikidata.org/w/api.php',{
        'action': 'wbsearchentities',
        'language': 'en',
        'type': 'property',
        'search': property,
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
        suggestion = wikipedia.suggest(words)
        if suggestion is not None:
            page = wikipedia.page(suggestion)
        else:
            return "\"" + words + "\" does not match any pages. Try another id!"

    print("page = " + page.title)
    return page.title


def get_all_q_codes(words: str):
    """
    gets the list of codes relevant to the searched words passed in parameters.
    :param words: string of searched words
    :return: list of q-codes with, for each, a short description of the linked page.
    """
    answer = get_q_number(item=words)
    title = wikipedia_suggestion(words)
    answer = get_q_number(item=title)
    for string in answer['search']:
        try:
            desc = string['description']
        except KeyError:
            desc = "No description available"
        print(string['id'] + " : " + desc)


def get_tests(item: str):
    resp = get('https://www.wikidata.org/w/api.php', {
        'action': 'query',
        'list': 'search',
        'srsearch': item,
        'format': 'json'

    }).json()

    return resp


def get_q_number2(item: str):
    """

    :param item:
    :return:
    """
    resp = get('https://www.wikidata.org/w/api.php',{
        'action': 'wbgetentities',
        'languages': 'en',
        'ids': item,
        'props': 'claims',
        'format': 'json'
    }).json()
######### TODO: étudier le json (on récupère tous les claims) pour voir comment itérer dessus. Fonction pour itérer dessus?
    return resp

# get_all_q_codes(words="Aristude Briand")
# get_all_q_codes("The U.S.")
# print(get_p_number("location"))


print(get_q_number2("Q30"))
