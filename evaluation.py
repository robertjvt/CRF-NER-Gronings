#!/usr/bin/python3

import csv
import os

import sklearn_crfsuite
from sklearn_crfsuite import metrics
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV


def evaluate_model(crf, X_test, y_test):
    '''
    Evaluates the trained model on f1-score, recall and precision.
    '''
    labels = list(crf.classes_)
    #labels.remove('O')
    y_pred = crf.predict(X_test)
    sorted_labels = sorted(labels, key=lambda name: (name[1:], name[0]))
    print(metrics.flat_classification_report(
        y_true=y_test, y_pred=y_pred, labels=sorted_labels, digits=3))


def label_transitions(transition_features):
    '''
    Puts all the most likely label transitions in a .csv file
    with the weight of the transitions.
    '''
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, 'output/label_transitions.csv')
    with open(file, 'w') as file:
        csv_writer = csv.writer(file, delimiter='\t', lineterminator='\n')
        csv_writer.writerow(('Label', 'Next label', 'Weight'))
        for (label, next_label), weight in transition_features:
            row = label, next_label, weight
            csv_writer.writerow(row)


def feature_transitions(state_features):
    '''
    Puts all the feature transitions in a .csv file with the weight
    of the specific feature.
    '''
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, 'output/feature_transitions.csv')
    with open(file, 'w') as file:
        csv_writer = csv.writer(file, delimiter='\t', lineterminator='\n')
        csv_writer.writerow(('Attribute', 'Label', 'Weight'))
        for (attribute, label), weight in state_features:
            row = attribute, label, weight
            csv_writer.writerow(row)


def hyperparameter_optimization(X_train, y_train, labels):
    '''
    Finetunes the model by conducting hyperparameter optimization
    with 3-fold cross validation. This means the best parameters
    are chosen for the best scores.
    '''
    crf = sklearn_crfsuite.CRF(
        algorithm = 'lbfgs',
        max_iterations = 100,
        all_possible_transitions = True
        )

    params_space = {
        'c1': scipy.stats.expon(scale=0.5),
        'c2': scipy.stats.expon(scale=0.5),
        }

    f1_scorer = make_scorer(metrics.flat_f1_score, average = 'weighted', labels = labels.remove('O'))

    rs = RandomizedSearchCV(crf, params_space,
                            cv = 3,
                            verbose = 1,
                            n_jobs = -1,
                            n_iter = 50,
                            scoring = f1_scorer)
    rs.fit(X_train, y_train)
    print('best params: ', rs.best_params_)
    print('best CV score: ', rs.best_score_)
    print('model size: ', rs.best_estimator_.size_)

    crf = rs.best_estimator_
    return crf
