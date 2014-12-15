# coding: utf-8

import os, sys
from lxml import etree
from collections import defaultdict
from collections import Counter

DELIMITERS = ',.!? '


def translate_min_new(swedish_sentence, swe_eng, eng_swe, bigrams):
    words = english_words_new(swedish_sentence, swe_eng, eng_swe)
    last_word = "<s>"
    output = translate_min_help_new(last_word, words, 0, bigrams)
    max = -sys.maxint
    max2 = -sys.maxint
    print output
    result_sentence = -1
    for index, sentence in enumerate(output):
        if (sentence[1] > max or (sentence[1] >= max and sentence[2] > max2)) :
            result_sentence = index
            max = sentence[1]
            max = sentence[2]
    if(result_sentence == -1):
        return "Could not translate."
    if(max <= 0):
        print "Sentence did not have a bigram path. Translation is random."
    return " ".join(output[result_sentence][0])

def translate_min_help_new(last_word, words, depth, bigrams,lastfailed=False):
    if depth == len(words):
        return [([], sys.maxint, sys.maxint)]
    possibles = possible_words(last_word, words[depth], bigrams, lastfailed)
    alternatives = []
    for word, frequency in possibles.most_common():
        result = translate_min_help_new(word, words, depth + 1, bigrams)
        for wordz, freq, freq2 in result:
            alternatives.append(([word] + wordz, min(frequency,freq), min(max(frequency,freq), freq2)))
    
    if len(alternatives) == 0:
        #print ("No bigrams for word {0} to {1}".format(last_word,words[depth]))
        result = translate_min_help_new("", words, depth+1, bigrams, True)  
        for wordz, freq, freq2 in result:    
            alternatives.append(([iter(words[depth]).next()] + wordz, 0, 0))

    return alternatives


def english_words_new(swedish_sentence, swe_eng, eng_swe):
    swedish_words = (word.lower().strip(DELIMITERS) for word in swedish_sentence.split())
    translation = []
    for word in swedish_words:
        translation.append(to_english_new(word, swe_eng, eng_swe))
    return translation


def to_english_new(swedish_word, swe_eng, eng_swe, include_inflections=False):
    eng_words = set(swe_eng.xpath(u".//word[ @value='{0}']/translation/@value".format(swedish_word)))
    #if(len(eng_words) == 0):
    eng_words.update(swe_eng.xpath(u".//word[paradigm/inflection/@value='{0}']/translation/@value".format(swedish_word)))
    swe_boj = set(swe_eng.xpath(u".//word[paradigm/inflection/@value='{0}' or @value='{0}']/@value".format(swedish_word)))
    swe_boj.update(swe_eng.xpath(u".//word[paradigm/inflection/@value='{0}' or @value='{0}']/paradigm/inflection/@value".format(swedish_word)))

    bojs = set()
    for words in swe_boj:
        for w in words.split('/'):
            for w2 in w.split(','):
                bojs.add(w2.strip(DELIMITERS))

    for boj in bojs:
        #eng_words.update(set(eng_swe.xpath(u".//word[translation/@value='{0}']/paradigm/inflection/@value".format(boj))))
        #eng_words.update(set(eng_swe.xpath(u".//word[translation/@value='{0}']/@value".format(boj))))
        pass
    output = set()
    for words in eng_words:
        for w in words.split('/'):
            for w2 in w.split(','):
                output.add(w2.strip(DELIMITERS))
    if len(output) == 0:
        print (u"No Translation for word {0}".format(swedish_word))
    return output









def get_inflections(word, dictionary):
    word = word.lower()
    L = dictionary.xpath(u".//word[paradigm/inflection/@value='{0}']/translation/@value".format(word))
    output = set(L)
    return output

def translate(swedish_sentence, dictionary, bigrams):
    last_word = "<s>"
    output = []
    for words in english_words(swedish_sentence, dictionary):
        possible = get_most_probable(last_word, words, bigrams)
        output.append(possible)
        last_word = possible
    return " ".join(output)

def translate_greedy(swedish_sentence, dictionary, bigrams):
    words = english_words(swedish_sentence, dictionary)
    last_word = "<s>"
    output = translate_greedy_help(last_word, words, 0, bigrams)
    return " ".join(output)

def translate_greedy_help(last_word, words, depth, bigrams):
    if depth == len(words):
        return []
    possibles = possible_words(last_word, words[depth], bigrams)
    for word in possibles.most_common():
        result = translate_greedy_help(word[0], words, depth + 1, bigrams)
        if result != None:
            return [word[0]] + result
    return None

def translate_sum(swedish_sentence, dictionary, bigrams):
    words = english_words(swedish_sentence, dictionary)
    last_word = "<s>"
    output = translate_sum_help(last_word, words, 0, bigrams)
    max = 0
    result_sentence = 0
    for index, sentence in enumerate(output):
        if sentence[1] > max:
            result_sentence = index
            max = sentence[1]
    return " ".join(output[result_sentence][0])

def translate_sum_help(last_word, words, depth, bigrams):
    if depth == len(words):
        return [([], 0)]
    possibles = possible_words(last_word, words[depth], bigrams)
    alternatives = []
    for word, frequency in possibles.most_common():
        result = translate_sum_help(word, words, depth + 1, bigrams)
        for wordz, freq in result:
            alternatives.append(([word] + wordz, frequency + freq))
    return alternatives

def translate_min(swedish_sentence, dictionary, bigrams):
    words = english_words(swedish_sentence, dictionary)
    last_word = "<s>"
    output = translate_min_help(last_word, words, 0, bigrams)
    max = 0
    result_sentence = 0
    for index, sentence in enumerate(output):
        if sentence[1] > max:
            result_sentence = index
            max = sentence[1]
    return " ".join(output[result_sentence][0])

def translate_min_help(last_word, words, depth, bigrams):
    if depth == len(words):
        return [([], sys.maxint)]
    possibles = possible_words(last_word, words[depth], bigrams)
    alternatives = []
    for word, frequency in possibles.most_common():
        result = translate_min_help(word, words, depth + 1, bigrams)
        for wordz, freq in result:
            alternatives.append(([word] + wordz, min(frequency, freq)))
    return alternatives


def possible_words(last_word, words, bigrams, ignoreLast=False):
    if(ignoreLast == False):
        possibles = Counter()
        for word in words:
            outword, frequency = get_most_probable_values(last_word, {word}, bigrams)
            if frequency > 0:
                possibles[outword] = frequency
        return possibles
    else:
        possibles = Counter()
        for word in words:
            possibles[word] = 0
        return possibles


def english_words(swedish_sentence, dictionary):
    swedish_words = (word.lower().strip(DELIMITERS) for word in swedish_sentence.split())
    translation = []
    for word in swedish_words:
        translation.append(to_english(word, dictionary))
    return translation


def to_english(swedish_word, dictionary, include_inflections=False):
    root = dictionary.getroot()
    english_words = set()
    for child in root:
        if child.attrib['value'].replace('(', '').replace(')', '') == swedish_word:
            for translation in child:
                if translation.tag == 'translation':
                    english_words.add(translation.attrib['value'].lower().strip(DELIMITERS))
    if len(english_words) == 0 or include_inflections: # Possible future arg
        english_words.update(get_inflections(swedish_word.lower().strip(DELIMITERS), dictionary))
    output = set()
    for words in english_words:
        for w in words.split('/'):
            for w2 in w.split(','):
                output.add(w2.strip(DELIMITERS))
    return output


def load_dictionary(filename):
    current_directory = os.path.dirname(__file__)
    lexikon = os.path.join(current_directory, 'data', filename)
    with open(lexikon, 'r') as f:
        parser = etree.XMLParser(encoding="utf-8")
        return etree.parse(f, parser=parser)

def get_most_probable(fr, to, dictionary):
    v1, v2 = get_most_probable_values(fr, to, dictionary)
    return v1

def get_most_probable_values(fr, to, dictionary):
    l = dictionary[fr].most_common()
    for v in l:
        if(v[0] in to):
            return v[0], v[1]
    return '', 0

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


if __name__ == '__main__':
    if sys.argv[1]:
        sentence = sys.argv[1].decode('utf-8')
        print(translate_min_new(sentence, load_dictionary("folkets_sv_en_public.xml"), load_dictionary("folkets_en_sv_public.xml"), load_bigrams()))
