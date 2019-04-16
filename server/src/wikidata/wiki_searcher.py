# wikipedia pages fetcher
import wikipedia
# html explorer
import bs4
# html fetcher through http
import urllib3
# signing certificates lib for http
import certifi
# suppresses warning of other libs (that we didn't raise ourselves)
import warnings

#
# Wikidata codes fetcher
#


class WikiSearcher:
    def __init__(self, words):
        self._words = words
        # ignores warning from Wikipedia package about its use of bs4
        warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')
        # ignores warning of unclosed socket, existing only in unittest (hence suppressed to have a clear
        warnings.filterwarnings("ignore", category=ResourceWarning)

# returns url of wikipedia page resulting of a search on words var
    def search_wikipedia(self):
        try:
            page = wikipedia.page(self._words)
        except wikipedia.exceptions.DisambiguationError as e:
            page = wikipedia.page(e.options[0])
        except wikipedia.exceptions.PageError as e:
            suggestion = wikipedia.suggest(self._words)
            if suggestion is not None:
                page = wikipedia.page(suggestion)
            else:
                return "\"" + self._words + "\" does not match any pages. Try another id!"

        return page.url

    def search_wikidata_q_label(self):
        url = self.search_wikipedia()
        if url.startswith("\""):
            return None
        else:
            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            html = http.request('GET', self.search_wikipedia())
            soup = bs4.BeautifulSoup(html.data, 'lxml')
            # extracting page code
            q_number_container = soup.find('li', {'id': 't-wikibase'})
            q_number = q_number_container.a['href'].rsplit('/')[-1]

            return q_number

    def set_words(self, words):
        self._words = words
