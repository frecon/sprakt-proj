# coding: utf-8

import os
from lxml import etree
from collections import defaultdict
from collections import Counter

DELIMITERS = ',.! '

def get_inflections(word, dictionary):
    word = word.lower()
    L = dictionary.xpath(u".//word[paradigm/inflection/@value='{0}']/translation/@value".format(word))
    output = set()
    for words in L:
        for w in words.split('/'):
            for w2 in w.split(','):
                output.add(w2.strip(DELIMITERS))
    return output

def translate(swedish_sentence, dictionary, bigrams):
    last_word = "<s>"
    output = []
    for words in english_words(swedish_sentence, dictionary):
        possible = get_most_probable(last_word, words, bigrams)
        output.append(possible)
        last_word = possible
    return " ".join(output)


def english_words(swedish_sentence, dictionary):
    swedish_words = (word.lower().strip(DELIMITERS) for word in swedish_sentence.split())
    translation = []
    for word in swedish_words:
        translation.append(to_english(word, dictionary))
    return translation


def to_english(swedish_word, dictionary):
    root = dictionary.getroot()
    english_words = set()
    for child in root:
        if child.attrib['value'].replace('(', '').replace(')', '') == swedish_word:
            for translation in child:
                if translation.tag == 'translation':
                    english_words.add(translation.attrib['value'].lower().strip(DELIMITERS))
    english_words.update(get_inflections(swedish_word.lower().strip(DELIMITERS), dictionary))
    return english_words


def load_dictionary():
    current_directory = os.path.dirname(__file__)
    lexikon = os.path.join(current_directory, 'data', 'folkets_sv_en_public.xml')
    with open(lexikon, 'r') as f:
        parser = etree.XMLParser(encoding="utf-8")
        return etree.parse(f, parser=parser)

def get_most_probable(fr, to, dictionary):
    l = dictionary[fr].most_common()
    for v in l:
        if(v[0] in to):
            return v[0]
    return ''
    

def load_bigrams():
    d = defaultdict(lambda : Counter())
    current_directory = os.path.dirname(__file__)
    bigrams = os.path.join(current_directory, 'data', 'count_2w.txt')
    with open(bigrams, 'r') as f:
        for line in f:
            fr, to, value = line.split()
            fr = fr.lower()
            to = to.lower()

            d[fr][to] += int(value)      
    return d

