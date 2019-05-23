import unittest
from wikidata.q_getter import get_all_q_codes, get_all_p_codes


def search_q_codes(words: str, expected_result: str) -> bool:
    result_list = get_all_q_codes(words)
    for result in result_list:
        if result[1] == expected_result:
            return True
    return False


class TestQGetter(unittest.TestCase):
    def test_get_all_q_codes(self):
        expected_result = "Q179888"
        # Searches with a well-written name
        self.assertTrue(search_q_codes("Aristide Briand", expected_result))

        # Searches with a typo error
        self.assertTrue(search_q_codes("Aristude Briand", expected_result))

        # Searches with a non existing word
        self.assertFalse(search_q_codes("erioereoiuzo", expected_result))
