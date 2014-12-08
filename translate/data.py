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


def loadBigrams():
    d = defaultdict(list)
    with open('data/count_2w.txt', 'r') as f:
        for line in f:
            split = line.split()
            d[split[0]].append((split[1], split[2]))
    return d
