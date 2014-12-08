import unittest
from translate.data import to_english

class TestDictionary(unittest.TestCase):
    def test_to_english_swedish_word_returns_list_of_english_words(self):
        actual = to_english('hej')
        expected = ['hello!', 'hallo!', 'Hey', 'Hi']
        self.assertEqual(actual, expected)
