import os
import xml.etree.ElementTree as ET

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

