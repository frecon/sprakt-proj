import unittest
from translate.data import (
    to_english,
    load_dictionary,
)

class TestData(unittest.TestCase):
    def test_to_english_swedish_word_returns_list_of_english_words(self):
        dictionary = load_dictionary()
        actual = to_english('hej', dictionary)
        expected = ['hello!', 'hallo!', 'Hey', 'Hi']
        self.assertEqual(actual, expected)



class TestDirectTranslate(unittest.TestCase):
    def test_direct_translate(self):
        pass

