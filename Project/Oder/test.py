#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
L=['A','B','C','D','E','F','G']
a=L[:4]
b=L[-2:]
print a
print b


c=[x*x for x in range(1,11)]
print c
[d for d in os.listdir('.')]
print d

#将该list中的非字符串去掉，然后再将大写字母转化成小写
L1=['Hello','World',18,'Apple',None]
L3=[]
for key in L1:
    if(isinstance(key,str))==True:
        L3.append(key)
L2=[s.lower() for s in L3]
print L2

