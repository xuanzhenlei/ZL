#!/usr/bin/python
#-*- coding:utf-8 -*-
# import os
# L=['A','B','C','D','E','F','G']
# a=L[:4]
# b=L[-2:]
# print a
# print b
#
#
# c=[x*x for x in range(1,11)]
# print c
# [d for d in os.listdir('.')]
# print d
#
# #将该list中的非字符串去掉，然后再将大写字母转化成小写
# L1=['Hello','World',18,'Apple',None]
# L3=[]
# for key in L1:
#     if(isinstance(key,str))==True:
#         L3.append(key)
# L2=[s.lower() for s in L3]
# print L2

import csv
fo=open('csv3.csv','w')
ifile=open('csv1.csv','rb')
reader=csv.reader(ifile)
ifile1=open('csv2.csv','rb')
reader1=csv.reader(ifile1)
flag=None
for row in reader:
    if(flag):
        row=' '.join(row)+"\n"
    else:
        row=' '.join(row)+' '
    fo.write(row)
    for row1 in reader1:
        if(row1!=None):
            row1=' '.join(row1)+"\n"
            fo.write(row1)
            flag=False
        else:
            flag=True
        break

ifile.close()
ifile1.close()
fo.close()

# import pandas as pd
#
# df=pd.read_csv(r'csv2.csv')
# dd=pd.read_csv(r'csv1.csv')
# data=pd.merge(df,dd,on=['show1'])
# data=data['show1','large','age','show2','name']
# print data
#
# import csv
# import pandas
#
# df=pandas.read_csv('csv1.csv')
# dd=pandas.read_csv('csv2.csv')
# data=pandas.merge(df,dd,on=['show1','show2'],how='inner')
# date=data[['show1','show2','name','age']]
# date.to_csv(r'data.csv',encoding='utf8')
