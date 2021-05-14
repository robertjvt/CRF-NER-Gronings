#!/usr/bin/python3

import csv


def main():
    with open('dorpen.csv', 'r', newline = '') as file:
        csv_reader = csv.reader(file, delimiter=';')
        data = list(csv_reader)

    plaatsnamen = []
    niet = []
    letters = ['A-z']    
    for item in data:
        for item2 in item:
            if item2 != '' and len(item2) != 1:
                item2 = item2.split()
                if len(item2) > 1:
                    plaatsnamen.append([item2[0], item2[1]])
    new_plaats = []
    for item in plaatsnamen:
        if item[1][0] != '(':
            new_plaats.append(item)
        else:
            new_plaats.append(item[0])
    for item in new_plaats:
        if isinstance(item, list):
            print(item[0], item[1])
        else:
            print(item)
                

if __name__ == "__main__":
    main()
