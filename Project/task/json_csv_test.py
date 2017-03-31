#!/usr/bin/python
#-*- coding:utf-8 -*-


# I=[{"publicdate": " 1996-12 ", "img": "https://img1.doubanio.com/mpic/s1070959.jpg", "author": "[清] 曹雪芹 著、高鹗 续 ", "rating_num": "9.5", "price": " 59.70元", "introduction": "《红楼梦》是一部百科全书式的长篇小说。以宝黛爱情悲剧为主线，以四大家族的荣辱兴衰为背景，描绘出18世纪中国封建社会的方方面面，以及封建专制下新兴资本主义民主...", "counts": "115296", "publicplace": " 人民文学出版社 ", "name": "红楼梦"},{"publicdate": " 2016-10 ", "img": "https://img1.doubanio.com/mpic/s29087849.jpg", "author": "袁珂 译注 ", "rating_num": "9.1", "price": " 49.80元", "introduction": "读懂《山海经》的权威实用版本 ★ 神话学大师袁珂先生在《山海经校注》的基础上，精炼了过于繁琐的学术性注释，增加了全文的白话翻译，将博大深奥的《山海经》变得浅...", "counts": "455", "publicplace": " 北京联合出版公司·后浪出版公司 ", "name": "山海经全译"}]
# with open('json_csv_test.csv','w') as file:
#     for d in I:
#         file.write('%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(d['author'],d['name'],d['publicplace'],d['publicdate'],d['price'],d['rating_num'],d['counts'],d['introduction'],d['img']))
#     file.close()


# I='{"publicdate": " 1996-12 ", "img": "https://img1.doubanio.com/mpic/s1070959.jpg", "author": "[清] 曹雪芹 著、高鹗 续 ", "rating_num": "9.5", "price": " 59.70元", "introduction": "《红楼梦》是一部百科全书式的长篇小说。以宝黛爱情悲剧为主线，以四大家族的荣辱兴衰为背景，描绘出18世纪中国封建社会的方方面面，以及封建专制下新兴资本主义民主...", "counts": "115296", "publicplace": " 人民文学出版社 ", "name": "红楼梦"},{"publicdate": " 2016-10 ", "img": "https://img1.doubanio.com/mpic/s29087849.jpg", "author": "袁珂 译注 ", "rating_num": "9.1", "price": " 49.80元", "introduction": "读懂《山海经》的权威实用版本 ★ 神话学大师袁珂先生在《山海经校注》的基础上，精炼了过于繁琐的学术性注释，增加了全文的白话翻译，将博大深奥的《山海经》变得浅...", "counts": "455", "publicplace": " 北京联合出版公司·后浪出版公司 ", "name": "山海经全译"}'
#
# R=eval(I)
# print R

# fo1=open('request.csv','r')
# #result = fo1.read()
# #row_str1= json.loads(result,encoding='utf-8')
# row_str1=eval(fo1)
# print row_str1


# fo1=open('request1.csv','r')
# line = file.readline()
# print row_str1
    # with open('json_csv_test.csv','w') as file:
    #     for d in result:
    #         #file.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(d['name'],d['img'],d['author'],d['rating_num'],d['price'],d['work'],d['trans1'],d['trans2'],d['introduction'],d['counts'],d['publicplace'],d['publicdate']))
    #         file.write('%d,%s,%d,%s,%s\n'%(d['name'],d['img'],d['rating_num'],d['introduction'],d['counts']))
    #     file.close()
    # fo1.close()





file = open('test111.csv','r')
file1=open('test1.csv','w')
lines = file.readlines()
for d in lines:
    d=eval(d)
    file1.write('%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(d['name'],d['img'],d['author'],d['rating_num'],d['price'],d['introduction'],d['counts'],d['publicplace'],d['publicdate']))
file1.close()


# file=open()
# while 1:
#     line = file.readline()
#     #print line
#     fo=open('test.csv','w')
#     fo.write('%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(line['name'],line['img'],line['author'],line['rating_num'],line['price'],line['introduction'],line['counts'],line['publicplace'],line['publicdate']))
#     if not line:
#         fo.close()
#         break
#     break





