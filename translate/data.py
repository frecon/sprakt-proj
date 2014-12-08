import os
import xml.etree.ElementTree as ET
from collections import defaultdict


def to_english(swedish_word):
    current_directory = os.path.dirname(__file__)
    lexikon = os.path.join(current_directory, 'data', 'folkets_sv_en_public.xml')
    tree = ET.parse(lexikon)
    root = tree.getroot()
    english_words = []
    for child in root:
        if child.attrib['value'] == swedish_word:
            for translation in child:
                if translation.tag == 'translation':
                    english_words.append(translation.attrib['value'])
    return english_words


def load_bigrams():
    d = defaultdict(list)
    current_directory = os.path.dirname(__file__)
    bigrams = os.path.join(current_directory, 'data', 'count_2w.txt')
    with open(bigrams, 'r') as f:
        for line in f:
            split = line.split()
            d[split[0]].append((split[1], split[2]))
    return d
