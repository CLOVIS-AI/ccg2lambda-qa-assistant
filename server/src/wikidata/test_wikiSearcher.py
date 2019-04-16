from unittest import TestCase
from wikidata.wiki_searcher import WikiSearcher


class TestWikiSearcher(TestCase):
    # will take some time
    def test_search_wikipedia(self):
        # only one result possible
        wiki_searcher = WikiSearcher("Aristide Briand")
        self.assertEqual("https://en.wikipedia.org/wiki/Aristide_Briand", wiki_searcher.search_wikipedia())

        # several results possible, picks the first available
        wiki_searcher.set_words("New York")
        self.assertEqual("https://en.wikipedia.org/wiki/New_York_City", wiki_searcher.search_wikipedia())

        # use of suggestion provided by Wikipedia (to correct minor typing errors)
        wiki_searcher.set_words("Aristude Briand")
        self.assertEqual("https://en.wikipedia.org/wiki/Aristide_Briand", wiki_searcher.search_wikipedia())

        # nonsense with no result
        nonsense = "erroeroeoreoreorer"
        wiki_searcher.set_words(nonsense)
        expected_err_msg = "\"" + nonsense + "\" does not match any pages. Try another id!"
        self.assertEqual(expected_err_msg, wiki_searcher.search_wikipedia())

    # admits that search_wikipedia works.
    def test_search_wikidata_label(self):
        # search for items (q-codes in wikidata)
        wiki_searcher = WikiSearcher("Aristide Briand")
        ar_briand_q_code = "Q179888"
        self.assertEqual(ar_briand_q_code, wiki_searcher.search_wikidata_q_label())

        wiki_searcher.set_words("Aristude Briand")
        self.assertEqual(ar_briand_q_code, wiki_searcher.search_wikidata_q_label())

        wiki_searcher.set_words("New York")
        self.assertEqual("Q60", wiki_searcher.search_wikidata_q_label())

        # should return no result
        wiki_searcher.set_words("erroeroereoreorero")
        self.assertEqual(None, wiki_searcher.search_wikidata_q_label())

        # search for fields (p-codes in wikidata). Is not supposed to work as it passes by wikipedia.
        # Must use instead a dictionary of all common fields.
        wiki_searcher.set_words("Instance of")
        self.assertNotEqual("P31", wiki_searcher.search_wikidata_q_label())
