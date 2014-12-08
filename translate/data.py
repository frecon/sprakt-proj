# coding: utf-8

import os
from xml.etree import ElementTree
from collections import defaultdict


def english_words(swedish_sentence):
    delimiters = ',.!'
    swedish_words = (word.lower().strip(delimiters) for word in swedish_sentence.split())
    translation = []
    dictionary = load_dictionary()
    for word in swedish_words:
        translation.append(to_english(word, dictionary))
    return translation


def to_english(swedish_word, dictionary):
    root = dictionary.getroot()
    english_words = []
    for child in root:
        if child.attrib['value'] == swedish_word:
            for translation in child:
                if translation.tag == 'translation':
                    english_words.append(translation.attrib['value'].lower())
    return english_words


def load_dictionary():
    current_directory = os.path.dirname(__file__)
    lexikon = os.path.join(current_directory, 'data', 'folkets_sv_en_public.xml')
    with open(lexikon, 'r') as f:
        parser = ElementTree.XMLParser(encoding="utf-8")
        return ElementTree.parse(f, parser=parser)


def load_bigrams():
    d = defaultdict(list)
    current_directory = os.path.dirname(__file__)
    bigrams = os.path.join(current_directory, 'data', 'count_2w.txt')
    with open(bigrams, 'r') as f:
        for line in f:
            split = line.split()
            d[split[0]].append((split[1], split[2]))
    return d
