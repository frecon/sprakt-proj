# coding: utf-8

import unittest
from collections import Counter
from translate.swedish_to_english import (
    to_english,
    load_dictionary,
    english_words,
    get_most_probable,
    load_bigrams,
    translate,
    get_inflections,
    translate_greedy,
    possible_words,
    translate_sum,
    translate_min,
    translate_min_new,
)

class TestData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dictionary = load_dictionary("folkets_sv_en_public.xml")
        cls.bigrams = load_bigrams()

    def test_to_english_feel(self):
        actual = to_english(u'mår', self.dictionary)
        expected = {'feel'}
        self.assertEqual(expected, actual)

    def test_to_english_tree(self):
        actual = to_english(u'träd', self.dictionary)
        expected = {'tree'}
        self.assertEqual(expected, actual)

    def test_to_english_allihopa(self):
        actual = to_english('allihopa', self.dictionary)
        expected = {'all', 'one and all'}
        self.assertEqual(expected, actual)

    def test_to_english_swedish_word_returns_list_of_english_words(self):
        actual = to_english('hej', self.dictionary)
        expected = {'hello', 'hallo', 'hey', 'hi'}
        self.assertEqual(expected, actual)

    def test_on(self):
        actual = to_english(u'på', self.dictionary)
        expected = {'at etc', 'on', 'in', 'during', 'of', 'at', 'after', 'in'}
        self.assertEqual(expected, actual)

    def test_ett(self):
        actual = to_english(u'ett', self.dictionary)
        expected = {'a', 'an', 'one'}
        self.assertEqual(expected, actual)

    def test_dig(self):
        actual = to_english(u'dig', self.dictionary)
        expected = {'you'}
        self.assertEqual(expected, actual)

    def test_direct_translate(self):
        swedish_sentence = u'Hej på dig.'
        actual = english_words(swedish_sentence, self.dictionary)

        expected = [{'hello', 'hallo', 'hey', 'hi'},
                   {'at etc', 'on', 'in', 'during', 'of', 'at', 'after', 'in'},
                    {'you'}]
        self.assertEqual(expected, actual)

    def test_get_most_probable_hi(self):
        fr = '<s>'
        to = ["hello", "hallo", "hi", "hey"]
        actual = get_most_probable(fr, to, self.bigrams)
        expected = 'hi'
        self.assertEqual(expected, actual)

    def test_get_most_probable_a(self):
        fr = 'that'
        to = ["a", "one"]
        actual = get_most_probable(fr, to, self.bigrams)
        expected = 'a'
        self.assertEqual(expected, actual)

    def test_get_most_probable_in(self):
        fr = 'active'
        to = ['on', 'and', 'in', 'yes', 'frej']
        actual = get_most_probable(fr, to, self.bigrams)
        expected = 'in'
        self.assertEqual(expected, actual)

    def test_translate_hi_all(self):
        swedish_sentence = u'Hej allihopa.'
        actual = translate(swedish_sentence, self.dictionary, self.bigrams)
        expected = 'hi all'
        self.assertEqual(expected, actual)

    def test_translate_how_are_you(self):
        swedish_sentence = u'Hur mår ni.'
        actual = translate(swedish_sentence, self.dictionary, self.bigrams)
        expected = 'how  '
        # XXX should fail due to semantical difference between SWE-ENG
        self.assertEqual(expected, actual)

    def test_translate_how_are_you_two(self):
        swedish_sentence = u'Är detta ett steg?'
        actual = translate_greedy(swedish_sentence, self.dictionary, self.bigrams)
        expected = 'is this one step'
        self.assertEqual(expected, actual)

    def test_translate_how_are_you_tree(self):
        swedish_sentence = u'Är detta ett träd?'
        actual = translate_greedy(swedish_sentence, self.dictionary, self.bigrams)
        expected = 'is this one tree'
        self.assertEqual(expected, actual)

    def test_xpath(self):
        actual = get_inflections(u'är', self.dictionary)
        expected = {'am/are/is'}
        # XXX should fail due to semantical difference between SWE-ENG
        self.assertEqual(expected, actual)

    def test_get_most_probable_a2(self):
        fr = 'this'
        to = ["a", "one"]
        actual = get_most_probable(fr, to, self.bigrams)
        expected = 'one'
        self.assertEqual(expected, actual)

    def test_possible_words(self):
        last_word = "<s>"
        swedish_sentence = u'Är detta ett träd?'
        words = english_words(swedish_sentence, self.dictionary)
        actual = possible_words(last_word, words[0], self.bigrams)
        expected = Counter({'is': 53121629, 'are': 26543233, 'am': 1596465})
        self.assertEqual(expected, actual)

    def test_translate_sum_is_this_a_tree(self):
        swedish_sentence = u'Är detta ett träd?'
        actual = translate_sum(swedish_sentence, self.dictionary, self.bigrams)
        expected = 'is this one tree'
        self.assertEqual(expected, actual)

    def test_translate_min_is_this_a_tree(self):
        swedish_sentence = u'Är detta ett träd?'
        actual = translate_min(swedish_sentence, self.dictionary, self.bigrams)
        expected = 'is this a tree'
        self.assertEqual(expected, actual)

    def test_translate_min_new(self):
        swedish_sentence = u'Jag hatar dig'
        actual = translate_min_new(swedish_sentence, self.dictionary, load_dictionary("folkets_en_sv_public.xml"), self.bigrams)
        expected = 'i hate you'
        self.assertEqual(expected, actual)
