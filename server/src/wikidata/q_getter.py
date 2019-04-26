#!/usr/bin/python3
from requests import get
# wikipedia pages fetcher
import wikipedia
# suppresses warning of other libs (that we didn't raise ourselves)
import warnings
# bot using wikidata API
from pywikibot import pagegenerators
import pywikibot


def get_q_number(wikiarticle):
    resp = get('https://www.wikidata.org/w/api.php', {
        'action': 'wbsearchentities',
        'language': 'en',
        'type': 'item',
        'search': wikiarticle,
        'format': 'json',
        'where': 'nearmatch'

    }).json()

    return resp


def wikipedia_suggestion(words):
    """
    returns url of wikipedia page resulting of a search on words var
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


def get_pages(words):
    site = pywikibot.page.PropertyPage()
    return resp


def get_all_q_codes(words):
    title = wikipedia_suggestion(words)
    answer = get_q_number(wikiarticle=title)
    for string in answer['search']:
        try:
            desc = string['description']
        except KeyError:
            desc = "No description available"
        print(string['id'] + " : " + desc)


# get_all_q_codes(words="Aristude Briand")
print(get_pages("Aristude Briand"))
