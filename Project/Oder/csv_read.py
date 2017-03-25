#!/usr/bin/python
#-*- coding:utf-8 -*-

import csv
rows = [['1', '2', '3'], ['4', '5', '6']]
with open('csv2.csv', 'w+') as csv_file:
    writer = csv.writer(csv_file)
    for row in rows:
        writer.writerow(row)

with open('csv2.csv', 'r+') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        print(str(row))
