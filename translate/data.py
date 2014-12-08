import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from collections import Counter


def to_english(swedish_word, dictionary):
    root = dictionary.getroot()
    english_words = []
    for child in root:
        if child.attrib['value'] == swedish_word:
            for translation in child:
                if translation.tag == 'translation':
                    english_words.append(translation.attrib['value'])
    return english_words


def load_dictionary():
    current_directory = os.path.dirname(__file__)
    lexikon = os.path.join(current_directory, 'data', 'folkets_sv_en_public.xml')
    return ET.parse(lexikon)

def get_most_probable(fr, to, dictionary):
    l = dictionary[fr].most_common()
    for v in l:
        if(to.count(v[0]) > 0):
            return v[0]
    

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
