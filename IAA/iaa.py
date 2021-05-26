#!/usr/bin/python3

import csv
from nltk.metrics.agreement import AnnotationTask


def fleiss_kappa(ratings, n):
    '''
    Computes the Fleiss' kappa measure for assessing the reliability of 
    agreement between a fixed number n of raters when assigning categorical
    ratings to a number of items.
    
    Args:
        ratings: a list of (item, category)-ratings
        n: number of raters
        k: number of categories
    Returns:
        the Fleiss' kappa score
    
    See also:
        http://en.wikipedia.org/wiki/Fleiss'_kappa
    '''
    items = set()
    categories = set()
    n_ij = {}
    
    for i, c in ratings:
        items.add(i)
        categories.add(c)
        n_ij[(i,c)] = n_ij.get((i,c), 0) + 1
    N = len(items)

    p_x = dict(((c, sum(n_ij.get((i, c), 0) for i in items) / (1)) for c in categories))
    print(p_x)
    
    p_j = dict(((c, sum(n_ij.get((i, c), 0) for i in items) / (1.0 * n * N)) for c in categories))
    P_i = dict(((i, (sum(n_ij.get((i, c), 0) ** 2 for c in categories) - n) / (n * (n - 1.0))) for i in items))
    P_bar = sum(P_i.values()) / (1.0 * N)
    P_e_bar = sum(value ** 2 for value in p_j.values())

    
    kappa = (P_bar - P_e_bar) / (1 - P_e_bar)
    
    return kappa


def main():
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p5 = []
    test = []
    with open('IAA.csv', 'r', newline = '') as file:
        csv.reader = csv.reader(file, delimiter='\t')
        i = 0
        for row in csv.reader:
            row.pop(0)
            for item in row:
                test.append((i, item))
            i+= 1
    print(test)
    print(fleiss_kappa(test, 5)) 

main()
