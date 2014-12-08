# coding: utf-8

import unittest
from translate.swedish_to_english import (
    to_english,
    load_dictionary,
    english_words,
    get_most_probable,
    load_bigrams,
    translate,
    get_inflections,
)

class TestData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dictionary = load_dictionary()
        cls.bigrams = load_bigrams()

    def test_to_english_feel(self):
        actual = to_english(u'mår', self.dictionary)
        expected = set(['feel'])
        self.assertEqual(actual, expected)

    def test_to_english_allihopa(self):
        actual = to_english('allihopa', self.dictionary)
        expected = set(['all', 'one and all'])
        self.assertEqual(actual, expected)

    def test_to_english_swedish_word_returns_list_of_english_words(self):
        actual = to_english('hej', self.dictionary)
        expected = set(['hello', 'hallo', 'hey', 'hi'])
        self.assertEqual(actual, expected)

    def test_on(self):
        actual = to_english(u'på', self.dictionary)
        expected = set(['at etc', 'on', 'in', 'during', 'of', 'at', 'after', 'in'])
        self.assertEqual(actual, expected)

    def test_ett(self):
        actual = to_english(u'ett', self.dictionary)
        expected = set(['a', 'an', 'one', 'a, an'])
        self.assertEqual(actual, expected)

    def test_dig(self):
        actual = to_english(u'dig', self.dictionary)
        expected = set(['you'])
        self.assertEqual(actual, expected)

    def test_direct_translate(self):
        swedish_sentence = u'Hej på dig.'
        actual = english_words(swedish_sentence, self.dictionary)

        expected = [set(['hello', 'hallo', 'hey', 'hi']),
                   set(['at etc', 'on', 'in', 'during', 'of', 'at', 'after', 'in']),
                    set(['you'])]
        self.assertEqual(actual, expected)

    def test_get_most_probable_hi(self):
        fr = '<s>'
        to = ["hello", "hallo", "hi", "hey"]
        actual = get_most_probable(fr, to, self.bigrams)
        expected = 'hi'
        self.assertEqual(actual, expected)

    def test_get_most_probable_a(self):
        fr = 'that'
        to = ["a", "one"]
        actual = get_most_probable(fr, to, self.bigrams)
        expected = 'a'
        self.assertEqual(actual, expected)

    def test_get_most_probable_in(self):
        fr = 'active'
        to = ['on', 'and', 'in', 'yes', 'frej']
        actual = get_most_probable(fr, to, self.bigrams)
        expected = 'in'
        self.assertEqual(actual, expected)

    def test_translate_hi_all(self):
        swedish_sentence = u'Hej allihopa.'
        actual = translate(swedish_sentence, self.dictionary, self.bigrams)
        expected = 'hi all'
        self.assertEqual(actual, expected)

    def test_translate_how_are_you(self):
        swedish_sentence = u'Hur mår ni.'
        actual = translate(swedish_sentence, self.dictionary, self.bigrams)
        expected = 'how  '
        # XXX should fail due to semantical difference between SWE-ENG
        self.assertEqual(actual, expected)

    def test_translate_how_are_you(self):
        swedish_sentence = u'Är detta ett träd?'
        actual = translate(swedish_sentence, self.dictionary, self.bigrams)
        expected = 'is this a tree'
        self.assertEqual(actual, expected)

    def test_xpath(self):
        actual = get_inflections(u'är', self.dictionary)
        expected = set(['is', 'am', 'are'])
        # XXX should fail due to semantical difference between SWE-ENG
        self.assertEqual(actual, expected)

    def test_get_most_probable_a2(self):
        fr = 'this'
        to = ["a", "one"]
        actual = get_most_probable(fr, to, self.bigrams)
        expected = 'a'
        self.assertEqual(actual, expected)