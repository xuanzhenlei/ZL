# -*- coding: utf-8 -*-
import csv

def getSortedValues(rows):
    sortedValues=[]
    keys=row.keys()
    keys.sort()
    for key in keys:
        sortedValues.append(row[key])
    return sortedValues


rows =  [{'Column1': 'xiaodeng', 'Column2': '1','Column3': '2'},
         {'Column1': 'fengmei', 'Column2': '3' ,'Column3': '4'},
         {'Column1': 'xiaochen', 'Column2': '5','Column3': '6'},
         {'Column1': 'xiaodong', 'Column2': '1','Column3': '2'},
         {'Column1': 'xiaowang', 'Column2': '1','Column3': '2'}]

names={'Column1':'name','Column2':'show1','Column3':'show2'}

fileobj=open('csv1.csv','wb')
fileobj.write('\xEF\xBB\xBF')

writer=csv.writer(fileobj)

sortedValues=getSortedValues(names)
writer.writerow(sortedValues)

for row in rows:
    sortedValues = getSortedValues(row)
    print sortedValues
    writer.writerow(sortedValues)
