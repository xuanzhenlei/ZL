#!/usr/bin/python
#-*- coding:utf-8 -*-

#test1
# flist=['pprojiect.csv','ppproject.csv']
# oflie=open('hebing.csv','w')
#
# for fr in flist:
#     for txt in open(fr,'r'):
#         oflie.write(txt)
# oflie.close()

#test2
# import csv
# #import glob
# fo=open('hebing1.csv','w')
# #list=glob.glob('pprojiect.csv','ppproject.csv')
# #list=glob.glob('*.csv')
#
# list=('pprojiect.csv','ppproject.csv')
# for file in list:
#     ifile=open(file,'rb')
#     reader=csv.reader(ifile)
#     #reader=csv.DictReader(ifile)
#     #column=[row for row in reader]
#     for row in reader:
#         row=':'.join(row)+"\n"
#         fo.write(row)
# ifile.close()
# fo.close()
#

# #test3

# import csv
# fo=open('hebing2.csv','w')
# list=['pprojiect.csv','ppproject.csv']
# for file in list:
#     ifile=open(file,'rb')
#     reader=csv.reader(ifile)
#     for row in reader:
#         row=':'.join(row)+"\n"
#         fo.write(row)
# ifile.close()
# fo.close()


#test4
import csv as csv
import numpy as np
import pandas as pd
df=pd.read_csv('sku有offer但是没采购过的数据_v3.csv',sep='\t')
dd=pd.read_csv('ppproject.csv',sep='\t')
data=pd.merge(df,dd,on=['sku'],how='left')
# data=data[heads+heads1]
data.to_csv('test.csv')

