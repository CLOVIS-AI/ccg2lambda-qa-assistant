import unittest
from wikidata.q_getter import get_all_q_codes, get_all_p_codes


def search_q_codes(words: str, expected_result: str) -> bool:
    result_list = get_all_q_codes(words)
    for result in result_list:
        if result[1] == expected_result:
            return True
    return False


def search_p_codes(words: str, expected_result: str) -> bool:
    result_list = get_all_p_codes(words)
    for result in result_list:
        if result[1] == expected_result:
            return True
    return False


class TestQGetter(unittest.TestCase):
    def test_get_all_q_codes(self):
        expected_result = "Q179888"
        # Search with a well-written name
        self.assertTrue(search_q_codes("Aristide Briand", expected_result))

        # Search with a typo error
        self.assertTrue(search_q_codes("Aristude Briand", expected_result))

        # Search with acronyms
        expected_result = "Q30"
        self.assertTrue(search_q_codes("usa", expected_result))
        self.assertTrue(search_q_codes("United States of America", expected_result))

        # Search with a non existing word
        self.assertFalse(search_q_codes("erioereoiuzo", expected_result))

    def test_get_all_p_codes(self):
        expected_result = "P31"
        # Search with directly the name of the property
        self.assertTrue(search_p_codes("instance of", expected_result))

        # Search with alias of the property
        self.assertTrue(search_p_codes("is a", expected_result))

        # Search with several possibilities expected
        expected_result = "P625"
        loc = "location"
        self.assertTrue(search_p_codes(loc, expected_result))
        expected_result = "P276"
        self.assertTrue(search_p_codes(loc, expected_result))

        # Search with a non existing word
        self.assertFalse(search_p_codes("erereeroereoreoire", expected_result))
