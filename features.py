#!/usr/bin/python3

import csv
import os
import re
import string


def create_gazetteer():
    '''
    Creates a gazetteer based on Dutch residential areas and
    all towns in Groningen.
    '''
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, 'data/nl_places.csv')
    gazetteer = []
    with open(file, 'r', newline = '') as file:
        csv_reader = csv.reader(file, delimiter=';')
        data = list(csv_reader)
        for row in data[1:]:
            for place in row:
                if place not in gazetteer:
                    gazetteer.append(place)
                    
    file = os.path.join(directory, 'data/gro_towns.csv')
    with open(file, 'r', newline = '') as file:
        csv_reader = csv.reader(file)
        for item in csv_reader:
            item = item[0]
            if item not in gazetteer:
                gazetteer.append(item)         
    return gazetteer

gazetteer = create_gazetteer()


def create_first_names():
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, 'data/voornamen.txt')
    with open(file, 'r', newline = '') as file:
        return file.read().splitlines()
            
first_names = create_first_names()


def wordshape(word):
    '''
    Creates a wordshape of a given word, based on capital letters,
    regular letters and digits.
    '''
    reshape1 = re.sub('[A-Z]', 'X', word)
    reshape2 = re.sub('[a-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff]', 'x', reshape1)
    reshape3 = re.sub('[0-9]', 'd', reshape2)
    return reshape3


def short_wordshape(wordshape):
    # Not in use.
    '''
    Creates the shorter version of the wordshape.
    '''
    short_wordshape = ''
    for letter in wordshape:
        if len(short_wordshape) == 0:
            short_wordshape = letter
        elif letter != short_wordshape[-1]:
            short_wordshape += letter
    return short_wordshape


def word_features(sent, i):
    '''
    Defines features for all words in a given sentence. Every word has features of
    its token and the token before and after it.
    '''
    # Features to add:
    #  - Word index in sentence / x
    #  - character level ngrams / x
    #  - brown clusters         / o
    
    word = sent[i][0]
    punctuation = string.punctuation

    features = {
        # Word shape & case features
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word.istitle()': word.istitle(),
        'word.isupper()': word.isupper(),
        'word.isdigit()': word.isdigit(),
        'word.wordshape()': wordshape(word),

        # Prefix and suffix features
        'word.suffix3': word[-3:],
        'word.suffix2': word[-2:],
        'word.prefix3': word[:3],
        'word.prefix2': word[:2],

        # Gazetteer
        'word.ingazetteer': True if word in gazetteer else False,
        #'word.infirstnames': True if word in first_names else False, decreased score
        }

    if i > 0:
        prev_word = sent[i-1][0]
        features.update({
            'prev_word.lower()': prev_word.lower(),
            'prev_word.istitle()': prev_word.istitle(),
            'prev_word.isupper()': prev_word.isupper(),
            'prev_word.isdigit()': prev_word.isdigit(),
            #'word.ingazetteer': True if prev_word + ' ' + word in gazetteer or features['word.ingazetteer'] is True else False,
            'prev_word.punct': True if prev_word in punctuation else False,
            })
    else:
        features['bos'] = True

    if i < len(sent) - 1:
        next_word = sent[i+1][0]
        features.update({
            'next_word.lower()': next_word.lower(),
            'next_word.istitle()': next_word.istitle(),
            'next_word.isupper()': next_word.isupper(),
            'next_word.isdigit()': next_word.isdigit(),
            'next_word.punct': True if next_word in punctuation else False,
            #'word.ingazetteer': True if word + ' ' + next_word in gazetteer or features['word.ingazetteer'] is True else False,
            })
    else:
        features['eos'] = True

    # Trigrams - did not give better results, but did increase execution time significantly.
    #if i > 1:
        # trigram = two_prev_word, prev_word, word
        # -2 -1 0
        #two_prev_word = sent[i-2][0]
        #features.update({
            #'-ngram:ingazetteer': True if trigram in gazetteer or features['-ngram:ingazetteer'] is True else False,
            #})
        
    #if i > 0 and i < len(sent) - 1:
        # trigram = prev_word, word, next_word
        # -1 0 1
        #features.update({
            #'-ngram:ingazetteer': True if trigram in gazetteer or features['-ngram:ingazetteer'] is True else False,
            #})
    
    #if i < len(sent) - 2:
        # trigram = word, next_word, two_next_word
        # 0 1 2
        #two_next_word = sent[i+2][0]
        #features.update({
            #'+ngram:ingazetteer': True if trigram in gazetteer or features['+ngram:ingazetteer'] is True else False,
            #})

    return features


def sentence_features(sent):
    '''
    Helper function to define features for every sentence.
    '''
    return [word_features(sent, i) for i in range(len(sent))]


def sentence_labels(sent):
    '''
    Helper function to return the label for every token in a sentence.
    '''
    return [label for token, label in sent]
