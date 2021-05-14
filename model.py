#!/usr/bin/python3

import csv
import time
import os

import sklearn
import sklearn_crfsuite
import joblib

import features
import evaluation

from collections import Counter

def open_data():
    '''
    Opens the train and test set and puts the data in two seperate lists.
    '''
    with open('gro-ner-train.csv', 'r', newline = '') as file:
        csv_reader = csv.reader(file, delimiter=';')
        train_data = list(map(tuple, csv_reader))
        train_data.append(())

    with open('gro-ner-test.csv', 'r', newline = '') as file:
        csv_reader = csv.reader(file, delimiter=';')
        test_data = list(map(tuple, csv_reader))
        test_data.append(())
    
    train_sents = []
    test_sents = []
    temp_list = []
    labels = ['B-PER', 'I-PER', 'B-LOC', 'I-LOC', 'B-ORG', 'I-ORG', 'B-MISC', 'I-MISC', 'O']
    for item in train_data:
        if len(item) == 2 and item[1].upper() in labels:
            temp_list.append((item[0], item[1].upper()))
        elif item == ():
            train_sents.append(temp_list)
            temp_list = []   
    for item in test_data:
        if len(item) == 2 and item[1].upper() in labels:
            temp_list.append((item[0], item[1].upper()))
        elif item == ():
            test_sents.append(temp_list)
            temp_list = []
    return train_sents, test_sents


def define_train_test(train_sents, test_sents):
    '''
    Extracts features and labels from the train and test sets and stores them in lists.
    '''
    X_train = [features.sentence_features(s) for s in train_sents]
    y_train = [features.sentence_labels(s) for s in train_sents]

    X_test = [features.sentence_features(s) for s in test_sents]
    y_test = [features.sentence_labels(s) for s in test_sents]
    return X_train, y_train, X_test, y_test


def train_model(X_train, y_train):
    '''
    Trains a conditional random fields model on the train features and labels.
    '''
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
        )
    crf.fit(X_train, y_train)
    return crf


def save_model(crf):
    '''
    Saves the trained model using joblib.
    '''
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, 'model/gro_ner_model.sav')
    joblib.dump(crf, file)



def main():
    starting_time = time.time()
    train_sents, test_sents = open_data()
    X_train, y_train, X_test, y_test = define_train_test(train_sents, test_sents)
    crf = train_model(X_train, y_train)
    evaluation.evaluate_model(crf, X_test, y_test)
    evaluation.label_transitions(Counter(crf.transition_features_).most_common())
    evaluation.feature_transitions(Counter(crf.state_features_).most_common())
    #best_crf = evaluation.hyperparameter_optimization(X_train, y_train, list(crf.classes_))
    #evaluation.evaluate_model(best_crf, X_test, y_test)
    save_model(crf)

    print('Execution time:', round(time.time() - starting_time, 3), 'seconds')

    
if __name__ == "__main__":
    main()
