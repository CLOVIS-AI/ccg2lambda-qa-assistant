from unittest import TestCase


class TestWikiSearcher(TestCase):
    # will take some time
    def test_search_wikipedia(self):
        from wikidata.wiki_searcher import search_wikipedia

        # only one result possible
        searched_words = "Aristide Briand"
        self.assertEqual("https://en.wikipedia.org/wiki/Aristide_Briand", search_wikipedia(searched_words))

        # several results possible, picks the first available
        searched_words = "New York"
        self.assertEqual("https://en.wikipedia.org/wiki/New_York_City", search_wikipedia(searched_words))

        # use of suggestion provided by Wikipedia (to correct minor typing errors)
        searched_words = "Aristude Briand"
        self.assertEqual("https://en.wikipedia.org/wiki/Aristide_Briand", search_wikipedia(searched_words))

        # nonsense with no result
        searched_words = "erroeroeoreoreorer"
        expected_err_msg = "\"" + searched_words + "\" does not match any pages. Try another id!"
        self.assertEqual(expected_err_msg, search_wikipedia(searched_words))

    # admits that search_wikipedia works.
    def test_search_wikidata_label(self):
        from wikidata.wiki_searcher import search_wikidata_q_label

        # search for items (q-codes in wikidata)
        searched_words = "Aristide Briand"
        ar_briand_q_code = "Q179888"
        self.assertEqual(ar_briand_q_code, search_wikidata_q_label(searched_words))

        searched_words = "Aristude Briand"
        self.assertEqual(ar_briand_q_code, search_wikidata_q_label(searched_words))

        searched_words = "New York"
        self.assertEqual("Q60", search_wikidata_q_label(searched_words))

        # should return no result
        searched_words = "erroeroereoreorero"
        self.assertEqual(None, search_wikidata_q_label(searched_words))
