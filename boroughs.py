#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 13 Warmup"""


import csv
import json

gradingscale = {'A':1, 'B':.9, 'C':.8, 'D':.7, 'F':.6}


def get_score_summary(filename):
    de_duplicate = {}
    start = 0
    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            start = start + 1
            if start == 1:
                continue
            # print(row)
            if len(row) > 10 and (row[10] != 'P' and row[10] != ''):
                key = "{0}, {1}, {2}".format(row[0], row[1], row[10])
                #print(key)
                if de_duplicate.has_key(key):
                    pass
                else:
                    de_duplicate[key] = row
    csvfile.close()
    # print("Size of dic {0} ".format(len(de_duplicate.keys())))
    res_data = {}
    for key, value in de_duplicate.iteritems():
        try:
            res_data[value[1]] = (res_data[value[1]][0]+1,
                                  res_data[value[1]][1] + float(value[9])
                                  * float(gradingscale[value[10]]))
        except:
            res_data[value[1]] = (1, float(value[9])
                                  * float(gradingscale[value[10]]))

    for key, value in res_data.iteritems():
        res_data[key] = (value[0], float(value[1]) / float(value[0]))
    return res_data


def get_market_density(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    # print(data['data'])
    data_dic = {}
    for i in range(0, len(data['data'])):
        key = data['data'][i][8].strip(" ")
        if data_dic.has_key(key):
            data_dic[key] = data_dic[key] + 1
        else:
            data_dic[key] = 1
    return data_dic


def correlate_data(file1, file2, file3):
    data1 = get_score_summary(file1)
    data2 = get_market_density(file2)
    sum = 0
    for key, value in data2.iteritems():
        sum = sum + float(value)
    data = {}
    for key, value in data2.iteritems():
        data[key.upper()] = (data1[key.upper()][1], float(value) / sum)
    with open(file3, 'w') as outfile:
        json.dump(data, outfile)
